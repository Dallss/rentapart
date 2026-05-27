"""
Management command: seed_mandaue_listings
Usage:
    python manage.py seed_mandaue_listings
    python manage.py seed_mandaue_listings --clear

Seeds realistic rental listings around Mandaue City, Cebu.
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
# Images
# ---------------------------------------------------------------------------

INTERIOR_IMAGES: list[tuple[str, str]] = [
    ("photo-1555041469-a586c61ea9bc", "Bright open-plan living room"),
    ("photo-1600585154340-be6161a56a0c", "Modern kitchen with island"),
    ("photo-1560448204-e02f11c3d0e2", "Spacious master bedroom"),
    ("photo-1631049307264-da0ec9d70304", "En-suite bathroom"),
    ("photo-1616047006789-b7af5afb8c20", "Cozy dining area"),
    ("photo-1586023492125-27b2c045efd7", "Home office nook"),
    ("photo-1600607687920-4e2a09cf159d", "Walk-in wardrobe"),
    ("photo-1484154218962-a197022b5858", "Kitchen detail"),
    ("photo-1556909114-f6e7ad7d3136", "Guest bedroom"),
    ("photo-1565538810643-b5bdb714032a", "Balcony view"),
    ("photo-1560185007-cde436f6a4d0", "Swimming pool"),
    ("photo-1594563703937-fdc640497dcd", "Rooftop terrace"),
    ("photo-1512918728675-ed5a9ecdebfd", "Condo skyline"),
    ("photo-1502005097973-6a7082348e28", "Bedroom sunrise"),
    ("photo-1600047509807-ba8f99d2cdde", "Scandinavian living room"),
    ("photo-1615874959474-d609969a20ed", "Luxury bathroom"),
    ("photo-1622372738946-62e02505feb3", "Minimalist desk setup"),
    ("photo-1560185127-6a6a1a8d5e5e", "Outdoor dining terrace"),
    ("photo-1630699144867-37acec97df5a", "Gym and fitness area"),
    ("photo-1582268611958-ebfd161ef9cf", "Infinity pool at dusk"),
]

EXTERIOR_IMAGES: list[tuple[str, str]] = [
    ("photo-1494526585095-c41746359bc6", "Building facade"),
    ("photo-1545324418-cc1a3fa10c00", "Gated compound"),
    ("photo-1598928506311-c55ded91a20c", "Landscaped garden"),
    ("photo-1570129477492-45c003edd2be", "Street view"),
    ("photo-1628592102751-ba83b0314276", "Cebu skyline"),
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
    ("Beachfront / Sea View", "anchor"),
]


# ---------------------------------------------------------------------------
# Listings
# ---------------------------------------------------------------------------

LISTINGS: list[dict] = [
    {
        "title": "Industrial Loft Condo Near Parkmall",
        "description": (
            "A stylish industrial-inspired loft unit just minutes from "
            "Parkmall and Cebu Doctors' University."
        ),
        "city": "Mandaue City",
        "neighborhood": "Bakilid",
        "street_address": "A. S. Fortuna Street, Bakilid",
        "country": "Philippines",
        "latitude": "10.3389",
        "longitude": "123.9172",
        "monthly_rent": "26000.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.CONDOMINIUM,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Gym / Fitness Center",
            "Security / CCTV",
            "Elevator",
            "Furnished",
            "Water Heater",
        ],
        "hero_image_index": 1,
    },

    {
        "title": "Affordable Bedspace for Call Center Agents",
        "description": (
            "Budget-friendly shared accommodation designed for BPO employees."
        ),
        "city": "Mandaue City",
        "neighborhood": "Banilad Border",
        "street_address": "Gov. M. Cuenco Avenue Extension",
        "country": "Philippines",
        "latitude": "10.3445",
        "longitude": "123.9148",
        "monthly_rent": "3800.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.BEDSPACE,
        "property_type": PropertyType.DORM,
        "amenities": [
            "WiFi",
            "Laundry Area",
            "Security / CCTV",
            "Furnished",
            "Air Conditioning",
        ],
        "hero_image_index": 8,
    },

    {
        "title": "Family Townhouse Near Oakridge Business Park",
        "description": (
            "Modern three-storey townhouse near Oakridge Business Park."
        ),
        "city": "Mandaue City",
        "neighborhood": "Casuntingan",
        "street_address": "Casuntingan Road, Mandaue City",
        "country": "Philippines",
        "latitude": "10.3332",
        "longitude": "123.9221",
        "monthly_rent": "52000.00",
        "bedrooms": 3,
        "bathrooms": 3,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.TOWNHOUSE,
        "amenities": [
            "Parking",
            "Air Conditioning",
            "Security / CCTV",
            "Backup Generator",
            "Laundry Area",
            "Pet-Friendly",
            "Water Heater",
        ],
        "hero_image_index": 7,
    },

    {
        "title": "Minimalist Studio Along Hernan Cortes",
        "description": (
            "Compact minimalist studio perfect for solo renters."
        ),
        "city": "Mandaue City",
        "neighborhood": "Hernan Cortes",
        "street_address": "Hernan Cortes Street, Mandaue City",
        "country": "Philippines",
        "latitude": "10.3258",
        "longitude": "123.9185",
        "monthly_rent": "14500.00",
        "bedrooms": 0,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.STUDIO,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Elevator",
            "Security / CCTV",
            "Furnished",
        ],
        "hero_image_index": 16,
    },

    {
        "title": "Warehouse Office Space Near Subangdaku",
        "description": (
            "Commercial warehouse-office hybrid for logistics or online sellers."
        ),
        "city": "Mandaue City",
        "neighborhood": "Subangdaku",
        "street_address": "North Reclamation Area, Subangdaku",
        "country": "Philippines",
        "latitude": "10.3360",
        "longitude": "123.9308",
        "monthly_rent": "85000.00",
        "bedrooms": 0,
        "bathrooms": 2,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.COMMERCIAL,
        "amenities": [
            "Parking",
            "Security / CCTV",
            "Backup Generator",
        ],
        "hero_image_index": 20,
    },

    {
        "title": "Cozy Apartment Near UCMed and Chong Hua Mandaue",
        "description": (
            "Comfortable apartment ideal for healthcare workers."
        ),
        "city": "Mandaue City",
        "neighborhood": "Tipolo",
        "street_address": "F. Cabahug Street Extension",
        "country": "Philippines",
        "latitude": "10.3208",
        "longitude": "123.9235",
        "monthly_rent": "17000.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.APARTMENT,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Security / CCTV",
            "Water Heater",
            "Laundry Area",
        ],
        "hero_image_index": 5,
    },
]


class Command(BaseCommand):
    help = "Seed realistic Mandaue rental listings."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete Mandaue listings before seeding.",
        )

    def handle(self, *args, **options):

        if options["clear"]:

            mandaue_listings = Listing.objects.filter(
                city="Mandaue City"
            )

            ListingImage.objects.filter(
                listing__in=mandaue_listings
            ).delete()

            mandaue_listings.delete()

            self.stdout.write(
                self.style.WARNING(
                    "Existing Mandaue listings cleared."
                )
            )

        # -------------------------------------------------------------------
        # Amenities
        # -------------------------------------------------------------------

        amenity_map: dict[str, Amenity] = {}

        for name, icon in AMENITIES:
            obj, _ = Amenity.objects.get_or_create(
                name=name,
                defaults={"icon": icon},
            )
            amenity_map[name] = obj

        # -------------------------------------------------------------------
        # Landlord
        # -------------------------------------------------------------------

        landlord_profile = self._get_or_create_landlord()

        # -------------------------------------------------------------------
        # Listings
        # -------------------------------------------------------------------

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
                    "listing_type": data["listing_type"],
                    "property_type": data["property_type"],
                    "hero_image": unsplash_url(
                        ALL_IMAGES[data["hero_image_index"]][0],
                        w=1200,
                        h=800,
                    ),
                },
            )

            listing.amenities.clear()

            for amenity_name in data.get("amenities", []):
                if amenity_name in amenity_map:
                    listing.amenities.add(
                        amenity_map[amenity_name]
                    )

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
                f"\nDone! {created_count} Mandaue listings created."
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