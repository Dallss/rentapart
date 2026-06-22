import time
import cloudinary
from cloudinary.utils import api_sign_request
from django.conf import settings


def generate_cloudinary_signature(user_id: int):
    timestamp = int(time.time())
    folder = f"user_{user_id}"

    params_to_sign = {
        "timestamp": timestamp,
        "folder": folder,
    }

    signature = api_sign_request(
        params_to_sign,
        api_secret=settings.CLOUDINARY["api_secret"]
    )

    return {
        "timestamp": timestamp,
        "signature": signature,
        "api_key": settings.CLOUDINARY["api_key"],
        "cloud_name": settings.CLOUDINARY["cloud_name"],
        "folder": folder,
    }