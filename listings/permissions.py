from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLandlordOrReadOnly(BasePermission):
    """
    - Anyone can read (GET)
    - Only landlords can write (POST, PUT, PATCH, DELETE)
    - On object level: only the owner landlord can edit/delete
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        # must be logged in and be a landlord
        return (
            request.user.is_authenticated and
            hasattr(request.user, "profile") and
            request.user.profile.is_landlord()
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # only the landlord who owns this listing
        return obj.landlord == request.user.profile