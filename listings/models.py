from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import Profile


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
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.city}"


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="listings/")
    is_primary = models.BooleanField(default=False)
