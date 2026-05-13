from django.db import models
from accounts.models import Profile


class Listing(models.Model):
    landlord = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="listings",
        limit_choices_to={"role": "landlord"}
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