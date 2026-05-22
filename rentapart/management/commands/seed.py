"""
Management command: seed_listings
Usage: python manage.py seed_listings [--clear]

Populates the database with realistic Cebu rental listings, amenities,
and listing images sourced from Unsplash's static CDN (no API key needed).
"""

import random

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from accounts.models import Profile
from listings.models import Amenity, Listing, ListingImage

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
User = get_user_model()


# ---------------------------------------------------------------------------
# Unsplash source images – each tuple is (unsplash_photo_id, caption)
# Using the /photos/{id}/download endpoint (free, no auth needed for display)
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
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w={w}&h={h}&q=80"


# ---------------------------------------------------------------------------
# Seed data
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

LISTINGS: list[dict] = [
    # --- IT Park / Cebu Business District ---
    {
        "title": "Modern Studio in the Heart of IT Park",
        "description": (
            "Wake up to panoramic city views in this sleek, fully furnished studio on the 22nd floor "
            "of a premium tower inside Cebu IT Park. Everything a young professional needs is at your "
            "doorstep — cafes, 24-hour convenience stores, and the BPO campuses of the Philippines' "
            "Silicon Valley. The unit features floor-to-ceiling windows, a queen-size Murphy bed, "
            "and a compact but well-equipped kitchen."
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
        "amenities": ["WiFi", "Air Conditioning", "Gym / Fitness Center", "Security / CCTV", "Elevator", "Concierge"],
        "hero_image_index": 0,
    },
    {
        "title": "Executive 2BR Condo — IT Park Tower Residences",
        "description": (
            "This well-appointed two-bedroom unit occupies a high floor in one of IT Park's newest "
            "residential towers. The open-plan layout connects a full-sized kitchen island to a "
            "generous living area finished with engineered hardwood floors. The master suite includes "
            "a walk-in wardrobe and a rain-shower en suite. A dedicated tandem parking slot and "
            "24/7 concierge service are included in the rent."
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
        "amenities": ["WiFi", "Air Conditioning", "Gym / Fitness Center", "Parking", "Security / CCTV",
                      "Elevator", "Concierge", "Water Heater", "Furnished"],
        "hero_image_index": 12,
    },
    # --- Banilad / Talamban ---
    {
        "title": "Charming 3BR House in Quiet Banilad Village",
        "description": (
            "Nestled inside a well-maintained subdivision, this single-storey bungalow sits on a "
            "300-sqm lot shaded by mature mango trees. The three bedrooms are airy and bright; "
            "the largest opens onto a covered lanai perfect for early morning coffee. "
            "A maid's quarter, a two-car garage, and a private deep-well water supply make daily "
            "life comfortable and worry-free. Near Sacred Heart School and Banilad Town Centre."
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
        "amenities": ["Air Conditioning", "Parking", "Pet-Friendly", "Laundry Area",
                      "Backup Generator", "Water Heater", "Furnished"],
        "hero_image_index": 3,
    },
    {
        "title": "Fully Furnished 1BR Near USC Talamban Campus",
        "description": (
            "Ideal for graduate students or young couples, this tidy one-bedroom apartment is a "
            "five-minute ride from USC's Talamban campus and just minutes from North Reclamation Area. "
            "The unit comes fully furnished with a queen bed, study desk, 43-inch smart TV, and "
            "a compact refrigerator. The building has a rooftop with a great view of Talamban hills "
            "and reliable fibre internet included in the rent."
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
        "amenities": ["WiFi", "Air Conditioning", "Security / CCTV", "Cable TV",
                      "Furnished", "Water Heater", "Rooftop Access"],
        "hero_image_index": 6,
    },
    # --- Mactan Island ---
    {
        "title": "Beachfront Villa in Mactan — Private Pool & Garden",
        "description": (
            "Live the island life in this sprawling four-bedroom villa just steps from the white "
            "sand beach of Lapu-Lapu City. The manicured tropical garden wraps around a 10-metre "
            "private plunge pool. Inside, the interiors blend Filipino craftsmanship — capiz shell "
            "light fixtures, rattan accents — with modern comforts like a full-sized Western kitchen "
            "and smart-home controls. Minutes from Mactan-Cebu International Airport and Shangri-La resort."
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
        "amenities": ["WiFi", "Air Conditioning", "Swimming Pool", "Parking", "Security / CCTV",
                      "Backup Generator", "Pet-Friendly", "Beachfront / Sea View", "Water Heater",
                      "Furnished", "Laundry Area"],
        "hero_image_index": 19,
    },
    {
        "title": "Cozy Sea-View Studio in Cordova, Mactan",
        "description": (
            "An affordable coastal retreat for the remote worker or couple seeking weekend tranquillity. "
            "This studio unit sits on the third floor of a boutique building in Cordova — catch the "
            "sunrise over the Hilutungan Channel from your private balcony. The kitchenette is fully "
            "equipped, and the building has its own jetty where residents can dock a small banca. "
            "Explore Olango Island Wildlife Sanctuary in under ten minutes by boat."
        ),
        "city": "Cordova",
        "neighborhood": "Poblacion, Cordova",
        "street_address": "Coastal Road, Cordova, Cebu",
        "country": "Philippines",
        "latitude": "10.2560",
        "longitude": "123.9680",
        "monthly_rent": "14500.00",
        "bedrooms": 0,
        "bathrooms": 1,
        "amenities": ["WiFi", "Air Conditioning", "Balcony", "Security / CCTV",
                      "Beachfront / Sea View", "Water Heater"],
        "hero_image_index": 9,
    },
    # --- Guadalupe / Mabolo ---
    {
        "title": "Spacious 2BR Condo in Guadalupe — City & Mountain Views",
        "description": (
            "Perched on the 18th floor of a well-established residential tower in Guadalupe, "
            "this two-bedroom unit captures dramatic views of both the Cebu City skyline and the "
            "Central Visayas mountain range. The layout is generously proportioned with a full "
            "dining area separate from the living room. Guadalupe's location makes it ideal for "
            "accessing Ayala Center, SM City, and Fuente Osmena — all within 15 minutes by car."
        ),
        "city": "Cebu City",
        "neighborhood": "Guadalupe",
        "street_address": "Guadalupe Tower, Archbishop Reyes Avenue",
        "country": "Philippines",
        "latitude": "10.3105",
        "longitude": "123.9000",
        "monthly_rent": "32000.00",
        "bedrooms": 2,
        "bathrooms": 1,
        "amenities": ["WiFi", "Air Conditioning", "Gym / Fitness Center", "Parking",
                      "Security / CCTV", "Elevator", "Water Heater", "Furnished"],
        "hero_image_index": 4,
    },
    {
        "title": "Homey 3BR Townhouse in Mabolo — Near Ayala",
        "description": (
            "A three-storey townhouse in a gated cluster community a short walk from Ayala Center Cebu. "
            "The ground floor features a spacious living and dining area that opens to a covered "
            "outdoor terrace — perfect for entertaining. Three bedrooms occupy the upper floors, "
            "each with its own split-type A/C unit. A dedicated helper's quarter and a two-car "
            "tandem garage complete this family-ready home."
        ),
        "city": "Cebu City",
        "neighborhood": "Mabolo",
        "street_address": "Mabolo Townhomes, General Maxilom Extension",
        "country": "Philippines",
        "latitude": "10.3220",
        "longitude": "123.9010",
        "monthly_rent": "55000.00",
        "bedrooms": 3,
        "bathrooms": 3,
        "amenities": ["Air Conditioning", "Parking", "Security / CCTV", "Backup Generator",
                      "Water Heater", "Laundry Area", "Furnished", "Pet-Friendly"],
        "hero_image_index": 7,
    },
    # --- South Cebu ---
    {
        "title": "Hillside Retreat — 2BR with Mountain View in Minglanilla",
        "description": (
            "Escape the city bustle in this serene two-bedroom home perched on a hillside in "
            "Minglanilla, just 20 minutes south of Cebu City. The wrap-around veranda commands "
            "sweeping views of the Cebu Strait and the mountains of Negros on a clear day. "
            "The property includes a productive vegetable and herb garden, a native bamboo gazebo, "
            "and ample parking. Ideal for families or remote workers craving calm."
        ),
        "city": "Minglanilla",
        "neighborhood": "Tungkop, Minglanilla",
        "street_address": "Hillcrest Drive, Minglanilla, Cebu",
        "country": "Philippines",
        "latitude": "10.2400",
        "longitude": "123.8000",
        "monthly_rent": "28000.00",
        "bedrooms": 2,
        "bathrooms": 2,
        "amenities": ["Air Conditioning", "Parking", "Pet-Friendly", "Backup Generator",
                      "Water Heater", "Laundry Area"],
        "hero_image_index": 5,
    },
    # --- Downtown / Colon ---
    {
        "title": "Heritage Loft Near Colon Street — Fully Renovated",
        "description": (
            "A rare gem in the historic core of Cebu City: a top-floor loft unit inside a "
            "Spanish-colonial-era shophouse that has been sensitively restored. "
            "Exposed brick walls, original wooden trusses, and antique capiz windows coexist "
            "with modern plumbing, a brand-new kitchen, and high-speed fibre internet. "
            "Step outside to find Colon Street — Asia's oldest — heritage churches, local markets, "
            "and the best lechon de cebu in the country."
        ),
        "city": "Cebu City",
        "neighborhood": "Colon District, Downtown",
        "street_address": "Colon Street, Cebu City",
        "country": "Philippines",
        "latitude": "10.2950",
        "longitude": "123.9020",
        "monthly_rent": "16000.00",
        "bedrooms": 1,
        "bathrooms": 1,
        "amenities": ["WiFi", "Air Conditioning", "Security / CCTV", "Furnished", "Water Heater"],
        "hero_image_index": 14,
    },
]


class Command(BaseCommand):
    help = "Seed the database with realistic Cebu rental listings."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing listings, images, and amenities before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data…")
            ListingImage.objects.all().delete()
            Listing.objects.all().delete()
            Amenity.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared listings, images, and amenities."))

        # ---- 1. Ensure amenities exist ----------------------------------------
        self.stdout.write("Creating amenities…")
        amenity_map: dict[str, Amenity] = {}
        for name, icon in AMENITIES:
            obj, _ = Amenity.objects.get_or_create(name=name, defaults={"icon": icon})
            amenity_map[name] = obj
        self.stdout.write(self.style.SUCCESS(f"  {len(amenity_map)} amenities ready."))

        # ---- 2. Ensure a landlord profile with manage_leases permission --------
        landlord_profile = self._get_or_create_landlord()

        # ---- 3. Create listings -----------------------------------------------
        self.stdout.write("Seeding listings…")
        created_count = 0

        for data in LISTINGS:
            listing, created = Listing.objects.get_or_create(
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
                    "hero_image": unsplash_url(
                        ALL_IMAGES[data["hero_image_index"]][0], w=1200, h=800
                    ),
                },
            )

            if created:
                # Attach amenities
                for amenity_name in data.get("amenities", []):
                    if amenity_name in amenity_map:
                        listing.amenities.add(amenity_map[amenity_name])

                # Attach 5–7 images (hero + random picks, no duplicates)
                hero_idx = data["hero_image_index"]
                pool = [i for i in range(len(ALL_IMAGES)) if i != hero_idx]
                chosen_indices = random.sample(pool, k=random.randint(4, 6))
                all_chosen = [hero_idx] + chosen_indices  # hero is always first

                for order, img_idx in enumerate(all_chosen):
                    photo_id, caption = ALL_IMAGES[img_idx]
                    ListingImage.objects.create(
                        listing=listing,
                        image_url=unsplash_url(photo_id),
                        caption=caption,
                    )

                created_count += 1
                self.stdout.write(f"  ✔ Created: {listing}")
            else:
                self.stdout.write(f"  – Skipped (exists): {listing}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! {created_count} new listing(s) created out of {len(LISTINGS)} total."
            )
        )

    # ---------------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------------

    def _get_or_create_landlord(self) -> Profile:
        """
        Returns a Profile whose user has the `manage_leases` permission on Profile.
        Creates a demo user if none exists.
        """
        ct = ContentType.objects.get_for_model(Profile)
        perm, _ = Permission.objects.get_or_create(
            content_type=ct,
            codename="manage_leases",
            defaults={"name": "Can manage leases"},
        )

        # Check for any existing qualifying profile
        qualifying = Profile.objects.filter(
            user__user_permissions=perm
        ).first() or Profile.objects.filter(
            user__groups__permissions=perm
        ).first()

        if qualifying:
            self.stdout.write(
                self.style.SUCCESS(f"  Using existing landlord profile: {qualifying}")
            )
            return qualifying

        # Create a demo landlord
        self.stdout.write("  No landlord profile found — creating demo landlord…")
        user, user_created = User.objects.get_or_create(
            username="demo_landlord",
            defaults={
                "email": "landlord@ceburentals.ph",
                "first_name": "Ramon",
                "last_name": "Dela Cruz",
                "is_staff": False,
            },
        )
        if user_created:
            user.set_password("cebu1234!")
            user.save()
            self.stdout.write(
                self.style.WARNING(
                    "  Created user 'demo_landlord' with password 'cebu1234!' — "
                    "change this in production!"
                )
            )

        user.user_permissions.add(perm)

        # get_or_create Profile (assuming a post-save signal or manual creation is needed)
        profile, _ = Profile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS(f"  Landlord profile ready: {profile}"))
        return profile