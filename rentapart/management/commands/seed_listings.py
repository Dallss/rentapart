"""
Management command: seed_listings
Usage: python manage.py seed_listings [--clear]

Populates the database with realistic Cebu rental listings, amenities,
and listing images sourced from Unsplash's static CDN.
"""

import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from accounts.models import Profile
from listings.models import (
    Amenity,
    Listing,
    ListingImage,
    ListingType,
    PropertyType,
)

User = get_user_model()

# ---------------------------------------------------------------------------
# Unsplash image sources
# ---------------------------------------------------------------------------

INTERIOR_IMAGES: list[tuple[str, str]] = [
    ("photo-1555041469-a586c61ea9bc", "Bright open-plan living room"),
    ("photo-1600585154340-be6161a56a0c", "Modern kitchen with island"),
    ("photo-1560448204-e02f11c3d0e2", "Spacious master bedroom"),
    ("photo-1631049307264-da0ec9d70304", "En-suite bathroom with rain shower"),
    ("photo-1616047006789-b7af5afb8c20", "Cozy dining area"),
    ("photo-1586023492125-27b2c045efd7", "Home office nook"),
    ("photo-1600607687920-4e2a09cf159d", "Walk-in wardrobe"),
    ("photo-1484154218962-a197022b5858", "Contemporary kitchen detail"),
    ("photo-1556909114-f6e7ad7d3136", "Guest bedroom"),
    ("photo-1565538810643-b5bdb714032a", "Balcony with city view"),
    ("photo-1560185007-cde436f6a4d0", "Swimming pool and deck"),
    ("photo-1594563703937-fdc640497dcd", "Rooftop garden terrace"),
    ("photo-1512918728675-ed5a9ecdebfd", "High-rise condo view"),
    ("photo-1502005097973-6a7082348e28", "Sunrise bedroom view"),
    ("photo-1600047509807-ba8f99d2cdde", "Scandinavian living room"),
    ("photo-1615874959474-d609969a20ed", "Matte black bathroom fixtures"),
    ("photo-1622372738946-62e02505feb3", "Minimalist desk setup"),
    ("photo-1560185127-6a6a1a8d5e5e", "Outdoor dining terrace"),
    ("photo-1630699144867-37acec97df5a", "Gym and fitness area"),
    ("photo-1582268611958-ebfd161ef9cf", "Infinity pool at dusk"),
]

EXTERIOR_IMAGES: list[tuple[str, str]] = [
    ("photo-1494526585095-c41746359bc6", "Building facade at golden hour"),
    ("photo-1545324418-cc1a3fa10c00", "Gated compound entrance"),
    ("photo-1598928506311-c55ded91a20c", "Tropical landscaped garden"),
    ("photo-1570129477492-45c003edd2be", "Street view of the property"),
    ("photo-1628592102751-ba83b0314276", "Cebu city skyline backdrop"),
]

ALL_IMAGES = INTERIOR_IMAGES + EXTERIOR_IMAGES


def unsplash_url(photo_id: str, w: int = 900, h: int = 600) -> str:
    return (
        f"https://images.unsplash.com/{photo_id}"
        f"?auto=format&fit=crop&w={w}&h={h}&q=80"
    )


# ---------------------------------------------------------------------------
# Amenities
# ---------------------------------------------------------------------------

AMENITIES = [
    ("WiFi", "wifi"),
    ("Air Conditioning", "wind"),
    ("Swimming Pool", "droplets"),
    ("Gym / Fitness Center", "dumbbell"),
    ("Parking", "car"),
    ("Security / CCTV", "shield"),
    ("Balcony", "layout"),
    ("Pet-Friendly", "paw-print"),
    ("Laundry Area", "loader"),
    ("Backup Generator", "zap"),
    ("Water Heater", "thermometer"),
    ("Cable TV", "tv"),
    ("Furnished", "sofa"),
    ("Elevator", "arrow-up"),
    ("Rooftop Access", "sun"),
    ("Concierge", "bell"),
    ("Children's Play Area", "smile"),
    ("Beachfront / Sea View", "anchor"),
]


# ---------------------------------------------------------------------------
# Listings
# ---------------------------------------------------------------------------

LISTINGS: list[dict] = [
    {
        "title": "Modern Studio in the Heart of IT Park",
        "description": (
            "Wake up to panoramic city views in this sleek, fully furnished "
            "studio inside Cebu IT Park."
        ),
        "city": "Cebu City",
        "neighborhood": "IT Park, Lahug",
        "street_address": "Intramed Building, Cebu IT Park, Apas",
        "country": "Philippines",
        "latitude": "10.3275",
        "longitude": "123.9050",
        "monthly_rent": "22000.00",
        "bedrooms": 0,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.STUDIO,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Gym / Fitness Center",
            "Security / CCTV",
            "Elevator",
            "Concierge",
        ],
        "hero_image_index": 0,
    },

    {
        "title": "Executive 2BR Condo — IT Park Tower Residences",
        "description": (
            "A premium two-bedroom condominium in the heart of Cebu IT Park."
        ),
        "city": "Cebu City",
        "neighborhood": "IT Park, Lahug",
        "street_address": "Tower 3, Cebu IT Park, Apas",
        "country": "Philippines",
        "latitude": "10.3280",
        "longitude": "123.9060",
        "monthly_rent": "45000.00",
        "bedrooms": 2,
        "bathrooms": 2,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.CONDOMINIUM,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Gym / Fitness Center",
            "Parking",
            "Security / CCTV",
            "Elevator",
            "Concierge",
            "Water Heater",
            "Furnished",
        ],
        "hero_image_index": 12,
    },

    {
        "title": "Charming 3BR House in Quiet Banilad Village",
        "description": (
            "A peaceful single-storey bungalow in a quiet Banilad subdivision."
        ),
        "city": "Cebu City",
        "neighborhood": "Banilad",
        "street_address": "Monteverde Street, Banilad",
        "country": "Philippines",
        "latitude": "10.3450",
        "longitude": "123.8970",
        "monthly_rent": "38000.00",
        "bedrooms": 3,
        "bathrooms": 2,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.HOUSE,
        "amenities": [
            "Air Conditioning",
            "Parking",
            "Pet-Friendly",
            "Laundry Area",
            "Backup Generator",
            "Water Heater",
            "Furnished",
        ],
        "hero_image_index": 3,
    },

    {
        "title": "Fully Furnished 1BR Near USC Talamban Campus",
        "description": (
            "Ideal for graduate students or young couples near USC Talamban."
        ),
        "city": "Cebu City",
        "neighborhood": "Talamban",
        "street_address": "Nivel Hills Road, Talamban",
        "country": "Philippines",
        "latitude": "10.3560",
        "longitude": "123.9100",
        "monthly_rent": "18000.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.APARTMENT,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Security / CCTV",
            "Cable TV",
            "Furnished",
            "Water Heater",
            "Rooftop Access",
        ],
        "hero_image_index": 6,
    },

    {
        "title": "Beachfront Villa in Mactan — Private Pool & Garden",
        "description": (
            "Luxury island living in a spacious beachfront villa in Mactan."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Punta Engaño, Mactan Island",
        "street_address": "Punta Engaño Road, Lapu-Lapu City",
        "country": "Philippines",
        "latitude": "10.2760",
        "longitude": "124.0110",
        "monthly_rent": "120000.00",
        "bedrooms": 4,
        "bathrooms": 4,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.HOUSE,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Swimming Pool",
            "Parking",
            "Security / CCTV",
            "Backup Generator",
            "Pet-Friendly",
            "Beachfront / Sea View",
            "Water Heater",
            "Furnished",
            "Laundry Area",
        ],
        "hero_image_index": 19,
    },

    {
        "title": "Affordable Bedspace Near USC Talamban",
        "description": (
            "Affordable shared student accommodation with WiFi and study area."
        ),
        "city": "Cebu City",
        "neighborhood": "Talamban",
        "street_address": "Gov. Cuenco Avenue, Talamban",
        "country": "Philippines",
        "latitude": "10.3580",
        "longitude": "123.9115",
        "monthly_rent": "4500.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.BEDSPACE,
        "property_type": PropertyType.DORM,
        "amenities": [
            "WiFi",
            "Laundry Area",
            "Security / CCTV",
            "Furnished",
        ],
        "hero_image_index": 8,
    },
]


class Command(BaseCommand):
    help = "Seed the database with Cebu rental listings."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing data before seeding.",
        )

    def handle(self, *args, **options):

        if options["clear"]:
            self.stdout.write("Clearing existing data...")

            ListingImage.objects.all().delete()
            Listing.objects.all().delete()
            Amenity.objects.all().delete()

            self.stdout.write(
                self.style.WARNING("Existing listings cleared.")
            )

        # -------------------------------------------------------------------
        # Amenities
        # -------------------------------------------------------------------

        self.stdout.write("Creating amenities...")

        amenity_map: dict[str, Amenity] = {}

        for name, icon in AMENITIES:
            obj, _ = Amenity.objects.get_or_create(
                name=name,
                defaults={"icon": icon},
            )
            amenity_map[name] = obj

        self.stdout.write(
            self.style.SUCCESS(f"{len(amenity_map)} amenities ready.")
        )

        # -------------------------------------------------------------------
        # Landlord profile
        # -------------------------------------------------------------------

        landlord_profile = self._get_or_create_landlord()

        # -------------------------------------------------------------------
        # Listings
        # -------------------------------------------------------------------

        self.stdout.write("Creating listings...")

        created_count = 0

        for data in LISTINGS:

            listing, created = Listing.objects.update_or_create(
                title=data["title"],
                defaults={
                    "landlord": landlord_profile,
                    "description": data["description"],
                    "country": data.get("country", "Philippines"),
                    "city": data["city"],
                    "neighborhood": data.get("neighborhood", ""),
                    "street_address": data.get("street_address", ""),
                    "latitude": data.get("latitude"),
                    "longitude": data.get("longitude"),
                    "monthly_rent": data["monthly_rent"],
                    "bedrooms": data["bedrooms"],
                    "bathrooms": data["bathrooms"],
                    "is_available": True,
                    "listing_type": data.get(
                        "listing_type",
                        ListingType.ENTIRE_PLACE,
                    ),
                    "property_type": data.get(
                        "property_type",
                        PropertyType.APARTMENT,
                    ),
                    "hero_image": unsplash_url(
                        ALL_IMAGES[data["hero_image_index"]][0],
                        w=1200,
                        h=800,
                    ),
                },
            )

            # -------------------------------------------------------------------
            # Sync amenities
            # -------------------------------------------------------------------

            listing.amenities.clear()

            for amenity_name in data.get("amenities", []):
                if amenity_name in amenity_map:
                    listing.amenities.add(
                        amenity_map[amenity_name]
                    )

            # -------------------------------------------------------------------
            # Sync images
            # -------------------------------------------------------------------

            ListingImage.objects.filter(
                listing=listing
            ).delete()

            hero_idx = data["hero_image_index"]

            pool = [
                i for i in range(len(ALL_IMAGES))
                if i != hero_idx
            ]

            chosen_indices = random.sample(
                pool,
                k=random.randint(4, 6),
            )

            all_chosen = [hero_idx] + chosen_indices

            for img_idx in all_chosen:

                photo_id, caption = ALL_IMAGES[img_idx]

                ListingImage.objects.create(
                    listing=listing,
                    image_url=unsplash_url(photo_id),
                    caption=caption,
                )

            if created:
                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"✔ Created: {listing}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"↻ Updated: {listing}"
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\nDone! {created_count} listings created."
                    )
                )

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _get_or_create_landlord(self) -> Profile:

        ct = ContentType.objects.get_for_model(Profile)

        perm, _ = Permission.objects.get_or_create(
            content_type=ct,
            codename="manage_leases",
            defaults={"name": "Can manage leases"},
        )

        qualifying = (
            Profile.objects.filter(
                user__user_permissions=perm
            ).first()
            or Profile.objects.filter(
                user__groups__permissions=perm
            ).first()
        )

        if qualifying:
            return qualifying

        user, created = User.objects.get_or_create(
            username="demo_landlord",
            defaults={
                "email": "landlord@ceburentals.ph",
                "first_name": "Ramon",
                "last_name": "Dela Cruz",
            },
        )

        if created:
            user.set_password("cebu1234!")
            user.save()

        user.user_permissions.add(perm)

        profile, _ = Profile.objects.get_or_create(user=user)

        return profile