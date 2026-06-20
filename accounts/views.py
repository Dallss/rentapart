from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response

from .models import Profile
from .serializers import GoogleAuthSerializer, ProfileSerializer

User = get_user_model()


def _username_for_google(sub: str, email: str) -> str:
    base = f"g_{sub}"
    if len(base) <= 150 and not User.objects.filter(username=base).exists():
        return base
    local = email.split("@")[0].replace(".", "_")[:120]
    candidate = f"{local}_{sub[:20]}"
    candidate = candidate[:150]
    n = 0
    while User.objects.filter(username=candidate).exists():
        n += 1
        suffix = f"_{n}"
        candidate = f"{candidate[: 150 - len(suffix)]}{suffix}"
    return candidate


def _user_payload(user, profile):
    return {
        "email": user.email,
        "username": user.username,
        "capabilities": {
            "leasing": profile.leasing_capabilities(),
        },
    }


def _manage_leases_permission():
    return Permission.objects.get(
        content_type=ContentType.objects.get_for_model(Profile),
        codename="manage_leases",
    )


class GoogleAuthView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        if not settings.GOOGLE_CLIENT_ID:
            return Response(
                {"detail": "Server is missing GOOGLE_CLIENT_ID configuration."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        ser = GoogleAuthSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        raw_token = ser.validated_data["id_token"]

        try:
            idinfo = google_id_token.verify_oauth2_token(
                raw_token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
        except ValueError:
            return Response(
                {"detail": "Invalid Google ID token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = idinfo.get("email")
        if not email:
            return Response(
                {"detail": "Google token did not include an email."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not idinfo.get("email_verified", False):
            return Response(
                {"detail": "Google email is not verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sub = idinfo.get("sub") or ""
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": _username_for_google(sub, email)},
        )
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])

        profile = user.profile

        refresh = RefreshToken.for_user(user)
        
        data = {
            "user": _user_payload(user, profile),
        }

        response = Response(data, status=status.HTTP_200_OK)
        
        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        print("VIEW HIT")
        print("AUTH HEADER:", request.headers.get("Authorization"))
        print("COOKIES:", request.COOKIES)

        return response


class GrantLeaseManagementView(APIView):
    """
    Optional upgrade: assign ``accounts.manage_leases`` to the user (idempotent).
    Same permission can be granted via Django admin or groups.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        perm = _manage_leases_permission()
        request.user.user_permissions.add(perm)
        user = User.objects.get(pk=request.user.pk)
        return Response(_user_payload(user, user.profile), status=status.HTTP_200_OK)


class JWTTokenRefreshView(TokenRefreshView):
    """Same as simplejwt refresh; exposed at /api/auth/token/refresh/."""

    pass
    

class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = ProfileSerializer(request.user.profile)

        return Response(
            {
                "profile": profile.data,
            }
        )


class Protected(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"Response": "u good"}, status=status.HTTP_200_OK)