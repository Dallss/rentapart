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
    role = models.CharField(max_length=10, choices=Role.choices, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def is_landlord(self):
        return self.role == self.Role.LANDLORD

    def has_role(self):
        return bool(self.role)

    def __str__(self):
        label = self.role or "no role"
        return f"{self.user.email} ({label})"