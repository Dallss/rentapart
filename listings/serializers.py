from rest_framework import serializers
from .models import Listing, ListingImage, Amenity


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name", "icon"]


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ["id", "image_url", "caption"]


class ListingSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        many=True,
        write_only=True,
        source="amenities",
    )
    images = ListingImageSerializer(many=True, read_only=True)
    landlord_name = serializers.CharField(source="landlord.user.get_full_name", read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "landlord",
            "landlord_name",
            "title",
            "description",
            # Address
            "country",
            "city",
            "neighborhood",
            "street_address",
            "latitude",
            "longitude",
            # Details
            "monthly_rent",
            "bedrooms",
            "bathrooms",
            "is_available",
            "amenities",
            "amenity_ids",
            "hero_image",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]