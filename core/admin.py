from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Listing, ListingImage, Application


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ["email", "username", "is_staff", "date_joined"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "phone"]
    list_filter = ["role"]


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", "city", "monthly_rent", "bedrooms", "is_available", "created_at"]
    list_filter = ["city", "is_available"]
    inlines = [ListingImageInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["renter", "listing", "status", "applied_at"]
    list_filter = ["status"]