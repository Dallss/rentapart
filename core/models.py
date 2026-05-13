from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Profile(models.Model):
    class Role(models.TextChoices):
        LANDLORD = "landlord", "Landlord"
        RENTER = "renter", "Renter"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=Role.choices)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def is_landlord(self):
        return self.role == self.Role.LANDLORD

    def __str__(self):
        return f"{self.user.email} ({self.role})"


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


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="applications")
    renter = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="applications",
        limit_choices_to={"role": "renter"}
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    message = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("listing", "renter")

    def __str__(self):
        return f"{self.renter} → {self.listing} [{self.status}]"