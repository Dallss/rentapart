from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import generate_cloudinary_signature


class CloudinarySignatureView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = generate_cloudinary_signature(request.user.id)
        return Response(data)