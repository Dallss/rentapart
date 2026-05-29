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

class ListingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "hero_image",
            "monthly_rent",
            "city",
            "bedrooms",
            "rating",
        ]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, "profile"):
            raise PermissionDenied("User does not have a profile.")
        serializer.save(landlord=user.profile)


class ListingDetailSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    landlord = serializers.CharField(source="landlord.user.get_full_name", read_only=True)
    listing_type = serializers.CharField(
        source="listing_type_label",
        read_only=True
    )    
    class Meta:
        model = Listing
        fields = "__all__"


class ListingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        exclude = ["landlord", "created_at", "updated_at", "id"]