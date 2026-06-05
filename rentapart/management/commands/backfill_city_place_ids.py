"""
Management command: backfill_place_ids
=======================================
Populates `city_google_place_id` for every Listing that is missing one,
using the Google Maps Places Autocomplete API (same service your frontend uses).

Usage
-----
    python manage.py backfill_place_ids

Options
-------
    --api-key   Your Google Maps API key (falls back to GOOGLE_MAPS_API_KEY env var)
    --dry-run   Print what would be updated without saving anything
    --limit N   Only process the first N listings (useful for testing)

Setup
-----
    Place this file at:
        <your_app>/management/commands/backfill_place_ids.py

    Make sure <your_app>/management/__init__.py and
    <your_app>/management/commands/__init__.py both exist (can be empty).

Requirements
------------
    pip install requests
"""

import os
import time
import logging

import requests
from django.core.management.base import BaseCommand, CommandError

from listings.models import Listing  # adjust import to your app name

logger = logging.getLogger(__name__)

AUTOCOMPLETE_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json"


def fetch_place_id(city: str, api_key: str) -> str | None:
    """
    Ask the Places Autocomplete API for the best match for `city`
    and return its place_id, or None if nothing suitable is found.
    """
    params = {
        "input": city,
        "types": "geocode",
        "components": "country:ph",
        "key": api_key,
    }

    try:
        response = requests.get(AUTOCOMPLETE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("HTTP error for %r: %s", city, exc)
        return None

    data = response.json()

    status = data.get("status")
    if status != "OK":
        logger.warning("API status %r for %r — %s", status, city, data.get("error_message", ""))
        return None

    predictions = data.get("predictions", [])
    if not predictions:
        return None

    # The first prediction is the best match
    return predictions[0]["place_id"]


class Command(BaseCommand):
    help = "Backfill city_google_place_id for Listing records that are missing it."

    def add_arguments(self, parser):
        parser.add_argument(
            "--api-key",
            type=str,
            default=None,
            help="Google Maps API key (defaults to GOOGLE_MAPS_API_KEY env var)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would be updated without writing to the database",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Maximum number of listings to process",
        )

    def handle(self, *args, **options):
        api_key = options["api_key"] or os.environ.get("GOOGLE_MAPS_API_KEY")
        if not api_key:
            raise CommandError(
                "No API key provided. Use --api-key or set GOOGLE_MAPS_API_KEY."
            )

        dry_run = options["dry_run"]
        limit = options["limit"]

        qs = Listing.objects.filter(
            city__isnull=False,
            city_google_place_id=""  # only those missing a place ID
        ).exclude(city="").order_by("id")

        if limit:
            qs = qs[:limit]

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS("Nothing to update — all listings already have a place ID."))
            return

        self.stdout.write(f"Processing {total} listing(s)  [dry_run={dry_run}]")

        updated = 0
        skipped = 0
        failed = 0

        for listing in qs:
            place_id = fetch_place_id(listing.city, api_key)

            if not place_id:
                self.stdout.write(
                    self.style.WARNING(
                        f"  [{listing.pk}] {listing.city!r} — no result, skipping"
                    )
                )
                failed += 1
                continue

            if dry_run:
                self.stdout.write(
                    f"  [{listing.pk}] {listing.city!r} → {place_id}  (dry run)"
                )
                skipped += 1
            else:
                listing.city_google_place_id = place_id
                listing.save(update_fields=["city_google_place_id"])
                self.stdout.write(
                    self.style.SUCCESS(f"  [{listing.pk}] {listing.city!r} → {place_id}")
                )
                updated += 1

            # Be kind to the API — 10 req/s is well within the free tier limit
            time.sleep(0.1)

        self.stdout.write("")
        self.stdout.write(f"Done. updated={updated}  skipped={skipped}  failed={failed}")