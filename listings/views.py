from rest_framework import viewsets, filters, permissions, mixins
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Listing
from .serializers import ListingListSerializer, ListingDetailSerializer, ListingWriteSerializer, ListingImageSerializer
from .permissions import IsLeaseManagerOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from django.db.models import Q
from .filters import ListingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Amenity


class ListingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLeaseManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_class = ListingFilter
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
        qs = Listing.objects.select_related("landlord__user").prefetch_related(
            "images", "amenities"
        )

        user = self.request.user

        if self.request.query_params.get("mine") == "true":
            if not user.is_authenticated:
                return qs.none()
            return qs.filter(landlord=user.profile)

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


    @action(detail=False, methods=["get"])
    def metadata(self, request):
        return Response({
            "amenities": list(
                Amenity.objects.order_by("name").values("id", "name", "icon")
            ),
            "listing_types": Listing._meta.get_field("listing_type").choices,
            "property_types": Listing._meta.get_field("property_type").choices,
        })

class ListingImageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = ListingImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(listing_id=self.kwargs["listing_pk"])