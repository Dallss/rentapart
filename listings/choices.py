from django.db import models

class ListingType(models.TextChoices):
   ENTIRE_PLACE = "entire_place", "Entire Place"
   PRIVATE_ROOM = "private_room", "Private Room"
   SHARED_ROOM = "shared_room", "Shared Room"
   BEDSPACE = "bedspace", "Bedspace"


class PropertyType(models.TextChoices):
   APARTMENT = "apartment", "Apartment"
   CONDOMINIUM = "condominium", "Condominium"
   HOUSE = "house", "House"
   TOWNHOUSE = "townhouse", "Townhouse"
   STUDIO = "studio", "Studio"
   DORM = "dorm", "Dormitory"
   OFFICE = "office", "Office"
   COMMERCIAL = "commercial", "Commercial"
   LOT = "lot", "Lot/Land"