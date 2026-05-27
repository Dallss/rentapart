from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Profile
from listings.models import Listing

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Assigns at least 3 listings per city to "
        "randallalquicer21@gmail.com"
    )

    EMAIL = "randallalquicer21@gmail.com"

    def handle(self, *args, **options):

        # -------------------------------------------------------------
        # Create or get user
        # -------------------------------------------------------------

        user, created = User.objects.get_or_create(
            email=self.EMAIL,
            defaults={
                "username": "randallalquicer21",
                "first_name": "Randall",
                "last_name": "Alquicer",
            },
        )

        # Ensure password exists if newly created
        if created:
            user.set_password("randall1234!")
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "Created landlord account."
                )
            )

        # -------------------------------------------------------------
        # Profile
        # -------------------------------------------------------------

        profile, _ = Profile.objects.get_or_create(user=user)

        # -------------------------------------------------------------
        # Cities to cover
        # -------------------------------------------------------------

        cities = [
            "Cebu City",
            "Mandaue City",
            "Lapu-Lapu City",
            "Cordova",
        ]

        updated_total = 0

        for city in cities:

            listings = (
                Listing.objects
                .filter(city=city)
                .order_by("created_at")[:3]
            )

            count = listings.count()

            if count == 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"No listings found for {city}"
                    )
                )
                continue

            for listing in listings:
                listing.landlord = profile
                listing.save(update_fields=["landlord"])

            updated_total += count

            self.stdout.write(
                self.style.SUCCESS(
                    f"Assigned {count} listings in {city}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Updated {updated_total} listings total."
            )
        )
