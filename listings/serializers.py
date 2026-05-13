from rest_framework import serializers
from .models import Listing, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ["id", "image", "is_primary"]


class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    landlord_email = serializers.EmailField(source="landlord.user.email", read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "address", "city",
            "monthly_rent", "bedrooms", "bathrooms", "is_available",
            "created_at", "images", "landlord_email"
        ]
        read_only_fields = ["created_at", "landlord_email"]