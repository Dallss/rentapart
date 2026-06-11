import django_filters
from .models import Listing


class ListingFilter(django_filters.FilterSet):
    min_rent = django_filters.NumberFilter(
        field_name="monthly_rent",
        lookup_expr="gte"
    )

    max_rent = django_filters.NumberFilter(
        field_name="monthly_rent",
        lookup_expr="lte"
    )

    q = django_filters.CharFilter(method="filter_q")

    class Meta:
        model = Listing
        fields = [
            "city_google_place_id",
            "bedrooms",
            "bathrooms",
            "is_available",
            "is_featured",
            "listing_type",
            "property_type",
            "is_furnished",
        ]

    def filter_q(self, queryset, name, value):
        from django.db.models import Q

        return queryset.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(city__icontains=value)
            | Q(neighborhood__icontains=value)
        )