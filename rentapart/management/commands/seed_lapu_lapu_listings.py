"""
Management command: seed_lapu_lapu_listings

Usage:
    python manage.py seed_lapu_lapu_listings
    python manage.py seed_lapu_lapu_listings --clear

Seeds realistic rental listings around Lapu-Lapu City and Cordova.
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
        "title": "Luxury Condo in Mactan Newtown with Sea View",
        "description": (
            "A premium fully furnished condominium unit overlooking the "
            "Mactan Channel."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Mactan Newtown",
        "street_address": "Newtown Boulevard, Punta Engaño",
        "country": "Philippines",
        "latitude": "10.3128",
        "longitude": "124.0152",
        "monthly_rent": "42000.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.CONDOMINIUM,
        "amenities": [
            "Swimming Pool",
            "Gym / Fitness Center",
            "WiFi",
            "Elevator",
            "Security / CCTV",
            "Furnished",
            "Concierge",
            "Water Heater",
        ],
        "hero_image_index": 12,
    },

    {
        "title": "Beachside Studio Near Shangri-La Mactan",
        "description": (
            "Compact beachfront studio ideal for digital nomads."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Punta Engaño",
        "street_address": "Punta Engaño Road",
        "country": "Philippines",
        "latitude": "10.3098",
        "longitude": "124.0201",
        "monthly_rent": "21000.00",
        "bedrooms": 0,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.STUDIO,
        "amenities": [
            "WiFi",
            "Swimming Pool",
            "Air Conditioning",
            "Security / CCTV",
            "Beachfront / Sea View",
            "Furnished",
        ],
        "hero_image_index": 19,
    },

    {
        "title": "Affordable Apartment in Marigondon",
        "description": (
            "Budget-friendly apartment near schools and transport."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Marigondon",
        "street_address": "Marigondon Crossing",
        "country": "Philippines",
        "latitude": "10.2805",
        "longitude": "123.9822",
        "monthly_rent": "9500.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.APARTMENT,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Laundry Area",
            "Security / CCTV",
        ],
        "hero_image_index": 5,
    },

    {
        "title": "Modern Townhouse Near Gaisano Grand Basak",
        "description": (
            "Family-ready townhouse close to supermarkets and schools."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Basak",
        "street_address": "Basak-Marigondon Road",
        "country": "Philippines",
        "latitude": "10.2862",
        "longitude": "123.9650",
        "monthly_rent": "32000.00",
        "bedrooms": 3,
        "bathrooms": 2,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.TOWNHOUSE,
        "amenities": [
            "Parking",
            "Air Conditioning",
            "Laundry Area",
            "Pet-Friendly",
            "Water Heater",
        ],
        "hero_image_index": 7,
    },

    {
        "title": "Shared Bedspace Near Mactan Doctors Hospital",
        "description": (
            "Affordable bedspace setup ideal for workers and students."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Basak",
        "street_address": "Basak Proper",
        "country": "Philippines",
        "latitude": "10.2920",
        "longitude": "123.9685",
        "monthly_rent": "3500.00",
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

    {
        "title": "Seaside Villa in Cordova with Private Pool",
        "description": (
            "Spacious tropical villa with direct sea access."
        ),
        "city": "Cordova",
        "neighborhood": "Gabi",
        "street_address": "Cordova Coastal Road",
        "country": "Philippines",
        "latitude": "10.2512",
        "longitude": "123.9490",
        "monthly_rent": "98000.00",
        "bedrooms": 4,
        "bathrooms": 4,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.HOUSE,
        "amenities": [
            "Swimming Pool",
            "Parking",
            "WiFi",
            "Beachfront / Sea View",
            "Pet-Friendly",
            "Laundry Area",
            "Furnished",
        ],
        "hero_image_index": 10,
    },

    {
        "title": "Coastal Studio Retreat in Cordova",
        "description": (
            "Minimalist coastal-inspired studio apartment."
        ),
        "city": "Cordova",
        "neighborhood": "Poblacion",
        "street_address": "Cordova Proper",
        "country": "Philippines",
        "latitude": "10.2558",
        "longitude": "123.9610",
        "monthly_rent": "14000.00",
        "bedrooms": 0,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.STUDIO,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Balcony",
            "Security / CCTV",
            "Water Heater",
        ],
        "hero_image_index": 9,
    },

    {
        "title": "Executive Condo Near Mactan Airport",
        "description": (
            "Executive condominium five minutes from MCIA."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Pusok",
        "street_address": "Airport Road, Pusok",
        "country": "Philippines",
        "latitude": "10.3100",
        "longitude": "123.9798",
        "monthly_rent": "28000.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.CONDOMINIUM,
        "amenities": [
            "WiFi",
            "Gym / Fitness Center",
            "Swimming Pool",
            "Elevator",
            "Furnished",
            "Security / CCTV",
        ],
        "hero_image_index": 4,
    },

    {
        "title": "Transit-Friendly Apartment Near Marina Mall",
        "description": (
            "Practical apartment ideal for airport workers."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Pusok",
        "street_address": "ML Quezon National Highway",
        "country": "Philippines",
        "latitude": "10.3081",
        "longitude": "123.9770",
        "monthly_rent": "12500.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.APARTMENT,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Laundry Area",
            "Security / CCTV",
        ],
        "hero_image_index": 2,
    },

    {
        "title": "Oceanfront Penthouse in Punta Engaño",
        "description": (
            "Ultra-luxury penthouse with panoramic ocean views."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Punta Engaño",
        "street_address": "Mactan Newtown Boulevard",
        "country": "Philippines",
        "latitude": "10.3139",
        "longitude": "124.0178",
        "monthly_rent": "185000.00",
        "bedrooms": 3,
        "bathrooms": 3,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.CONDOMINIUM,
        "amenities": [
            "Swimming Pool",
            "Gym / Fitness Center",
            "Concierge",
            "Parking",
            "WiFi",
            "Beachfront / Sea View",
            "Furnished",
            "Elevator",
            "Security / CCTV",
        ],
        "hero_image_index": 18,
    },

    {
        "title": "Private Beach House in Buyong",
        "description": (
            "Exclusive beach house with direct shoreline access."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Buyong",
        "street_address": "Buyong Beach Road",
        "country": "Philippines",
        "latitude": "10.2968",
        "longitude": "124.0065",
        "monthly_rent": "150000.00",
        "bedrooms": 5,
        "bathrooms": 4,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.HOUSE,
        "amenities": [
            "Swimming Pool",
            "Parking",
            "WiFi",
            "Beachfront / Sea View",
            "Pet-Friendly",
            "Laundry Area",
            "Furnished",
            "Security / CCTV",
        ],
        "hero_image_index": 21,
    },

    {
        "title": "Student-Friendly Dormitory Near LLC",
        "description": (
            "Simple but clean dormitory accommodation."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Gun-ob",
        "street_address": "Gun-ob Proper",
        "country": "Philippines",
        "latitude": "10.3190",
        "longitude": "123.9482",
        "monthly_rent": "3000.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.BEDSPACE,
        "property_type": PropertyType.DORM,
        "amenities": [
            "WiFi",
            "Laundry Area",
            "Security / CCTV",
        ],
        "hero_image_index": 6,
    },

    {
        "title": "Compact Rental Unit in Babag",
        "description": (
            "Affordable compact apartment near transport and markets."
        ),
        "city": "Lapu-Lapu City",
        "neighborhood": "Babag",
        "street_address": "Babag II Road",
        "country": "Philippines",
        "latitude": "10.3250",
        "longitude": "123.9565",
        "monthly_rent": "8500.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "listing_type": ListingType.ENTIRE_PLACE,
        "property_type": PropertyType.APARTMENT,
        "amenities": [
            "WiFi",
            "Air Conditioning",
            "Security / CCTV",
        ],
        "hero_image_index": 14,
    },
]


class Command(BaseCommand):
    help = "Seed realistic Lapu-Lapu and Cordova listings."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing Lapu-Lapu listings before seeding.",
        )

    def handle(self, *args, **options):

        if options["clear"]:

            lapu_listings = Listing.objects.filter(
                city__in=["Lapu-Lapu City", "Cordova"]
            )

            ListingImage.objects.filter(
                listing__in=lapu_listings
            ).delete()

            lapu_listings.delete()

            self.stdout.write(
                self.style.WARNING(
                    "Existing Lapu-Lapu listings cleared."
                )
            )

        amenity_map: dict[str, Amenity] = {}

        for name, icon in AMENITIES:
            obj, _ = Amenity.objects.get_or_create(
                name=name,
                defaults={"icon": icon},
            )
            amenity_map[name] = obj

        landlord_profile = self._get_or_create_landlord()

        created_count = 0

        for data in LISTINGS:

            listing, created = Listing.objects.update_or_create(
                title=data["title"],
                defaults={
                    "landlord": landlord_profile,
                    "description": data["description"],
                    "country": data["country"],
                    "city": data["city"],
                    "neighborhood": data["neighborhood"],
                    "street_address": data["street_address"],
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "monthly_rent": data["monthly_rent"],
                    "bedrooms": data["bedrooms"],
                    "bathrooms": data["bathrooms"],
                    "listing_type": data["listing_type"],
                    "property_type": data["property_type"],
                    "hero_image": unsplash_url(
                        ALL_IMAGES[data["hero_image_index"]][0],
                        w=1200,
                        h=800,
                    ),
                    "is_available": True,
                },
            )

            listing.amenities.clear()

            for amenity_name in data["amenities"]:
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
                f"\nDone! {created_count} listings created."
            )
        )

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