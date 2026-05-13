from django.shortcuts import render

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Listing
from .serializers import ListingSerializer
from .permissions import IsLandlordOrReadOnly


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [IsLandlordOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # GET /listings/?city=amsterdam&bedrooms=2
    filterset_fields = ["city", "bedrooms", "bathrooms", "is_available"]

    # GET /listings/?search=cozy
    search_fields = ["title", "description", "address"]

    # GET /listings/?ordering=monthly_rent
    ordering_fields = ["monthly_rent", "created_at", "bedrooms"]
    ordering = ["-created_at"]  # default

    def get_queryset(self):
        return Listing.objects.filter(is_available=True).select_related(
            "landlord__user"
        ).prefetch_related("images")

    def perform_create(self, serializer):
        # auto-attach the logged-in landlord's profile
        serializer.save(landlord=self.request.user.profile)