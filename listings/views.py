from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Listing
from .serializers import ListingListSerializer, ListingDetailSerializer, ListingWriteSerializer
from .permissions import IsLeaseManagerOrReadOnly


class ListingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLeaseManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["city", "bedrooms", "bathrooms", "is_available"]
    search_fields = ["title", "description"]
    ordering_fields = ["monthly_rent", "created_at", "bedrooms"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        mapping = {
            "list": ListingListSerializer,
            "retrieve": ListingDetailSerializer,
            "create": ListingWriteSerializer,
            "update": ListingWriteSerializer,
            "partial_update": ListingWriteSerializer,
        }

        return mapping.get(self.action, ListingListSerializer)
        
    def get_queryset(self):
        qs = Listing.objects.select_related(
            "landlord__user"
        ).prefetch_related(
            "images",
            "amenities",
        )
        # Non-authenticated users and regular users only see available listings
        # Lease managers and admins see everything
        user = self.request.user
        if not user.is_authenticated or not (
            user.is_staff or user.has_perm("accounts.manage_leases")
        ):
            qs = qs.filter(is_available=True)

        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, "profile"):
            raise PermissionDenied("User does not have a profile.")
        serializer.save(landlord=user.profile)