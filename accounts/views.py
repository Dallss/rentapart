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
import re

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

        if not email or not idinfo.get("email_verified", False):
            return Response(
                {"detail": "Verified Google email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sub = idinfo.get("sub") or ""
        picture = idinfo.get("picture")
        name = idinfo.get("name")
        given_name = idinfo.get("given_name", "")
        family_name = idinfo.get("family_name", "")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": _username_for_google(sub, email),
                "first_name": given_name,
                "last_name": family_name,
            },
        )

        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])

        profile, _ = Profile.objects.get_or_create(user=user)

        if created:
            update_fields = []
            if picture:
                profile.avatar_url = picture
                update_fields.append("avatar_url")
            if name:
                profile.display_name = name
                update_fields.append("display_name")
            if update_fields:
                profile.save(update_fields=update_fields)

        profile = user.profile

        refresh = RefreshToken.for_user(user)

        data = {
            "user": _user_payload(user, profile),
            "needs_onboarding": profile.needs_onboarding,
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

        return response


class OnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = request.user.profile

        display_name = request.data.get("display_name")
        birthday = request.data.get("birthday")
        phone = request.data.get("phone")

        missing = {}
        PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")


        if not profile.display_name and not display_name:
            missing["display_name"] = "This field is required"

        if not profile.birthday and not birthday:
            missing["birthday"] = "This field is required"
        
        if not profile.phone and not phone:
            missing["phone"] = "This field is required"

        elif not PHONE_REGEX.match(phone):
            missing["phone"] = "Invalid phone number format"

        if missing:
            return Response(
                {
                    "detail": "Onboarding incomplete",
                    "missing_fields": missing
                },
                status=400,
            )

        profile.display_name = display_name
        profile.birthday = birthday
        profile.phone = phone
        profile.save()

        return Response({
            "success": True,
            "profile": {
                "display_name": profile.display_name,
                "birthday": profile.birthday,
                "phone": profile.phone,
            },
            "needs_onboarding": False,
        })
        
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