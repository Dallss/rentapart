from django.db import models
from accounts.models import Profile
from listings.models import Listing


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="applications")
    renter = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    message = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("listing", "renter")

    def __str__(self):
        return f"{self.renter} → {self.listing} [{self.status}]"