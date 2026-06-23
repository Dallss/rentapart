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
    # TODO: rename db field to lat and lng
    lat = serializers.FloatField(source="latitude")
    lng = serializers.FloatField(source="longitude")
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
            "lat",
            "lng"
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
    amenities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Amenity.objects.all()
    )

    city_google_place_id = serializers.CharField(
        required=True,
        allow_blank=False
    )

    hero_image_url = serializers.URLField(
        source="hero_image",
        required=True,
        allow_blank=False
    )

    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "country",
            "city",
            "city_google_place_id",
            "neighborhood",
            "street_address",
            "monthly_rent",
            "bedrooms",
            "bathrooms",
            "is_furnished",
            "amenities",
            "hero_image_url",
            "listing_type",
            "property_type",
            "is_unfinished",
        ]