from django.contrib.auth.models import AbstractUser
from django.db import models

# Use with user.has_perm(...) — matches Profile.Meta.permissions codename.
MANAGE_LEASES_PERMISSION = "accounts.manage_leases"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Profile(models.Model):
    """
    One identity per user. Leasing: everyone is a lessee by default; creating and
    managing listings requires the ``accounts.manage_leases`` permission (grant
    via API upgrade, admin, or groups).
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    class Meta:
        permissions = [
            ("manage_leases", "Can create and manage lease listings"),
        ]

    def can_manage_leases(self):
        return self.user.has_perm(MANAGE_LEASES_PERMISSION)

    def leasing_capabilities(self):
        """Returned in API payloads; aligns with Django auth checks."""
        return {
            "lessee": True,
            "manage": self.can_manage_leases(),
        }

    def __str__(self):
        mode = "manage" if self.can_manage_leases() else "lessee"
        return f"{self.user.email} (leasing:{mode})"
