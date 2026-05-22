from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from accounts.models import Profile
from .choices import ListingType, PropertyType

def _lease_manager_profiles_q():
    ct = ContentType.objects.get_for_model(Profile)
    perm = Permission.objects.filter(content_type=ct, codename="manage_leases").first()
    if perm is None:
        return models.Q(pk__in=[])
    return models.Q(user__user_permissions=perm) | models.Q(
        user__groups__permissions=perm,
    )

class Listing(models.Model):
    landlord = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="listings",
        limit_choices_to=_lease_manager_profiles_q,
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    # Address
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100, blank=True)

    street_address = models.CharField(max_length=255, blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Details
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    amenities = models.ManyToManyField("Amenity", blank=True, related_name="listings")
    hero_image = models.URLField(blank=True)

    listing_type = models.CharField(
        max_length=30,
        choices=ListingType.choices,
        blank=True
    )

    property_type = models.CharField(
        max_length=30,
        choices=PropertyType.choices,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.city}"

class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image_url = models.URLField()
    caption = models.CharField(max_length=255, blank=True)

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "amenities"
        ordering = ["name"]