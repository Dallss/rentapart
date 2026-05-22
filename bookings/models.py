from django.db import models
from listings.models import Listing
from accounts.models import Profile

class Booking(models.Model):
   listing = models.ForeignKey(
      Listing,
      on_delete=models.CASCADE,
      related_name="bookings"
   )
   booker = models.ForeignKey(
      Profile,
      on_delete=models.CASCADE,
      related_name="bookings",
   )
   date       = models.DateField()
   start_time = models.TimeField()
   end_time   = models.TimeField()

   class Meta:
      constraints = [
         models.CheckConstraint(
               check=models.Q(end_time__gt=models.F("start_time")),
               name="booking_end_after_start",
         )
      ]

   def clean(self):
      if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

   def __str__(self):
      return f"{self.booker} → {self.listing} on {self.date} ({self.start_time}–{self.end_time})"