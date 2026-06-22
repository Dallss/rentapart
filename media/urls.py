from django.urls import path
from .views import CloudinarySignatureView

urlpatterns = [
    path("cloudinary/signature/", CloudinarySignatureView.as_view()),
]