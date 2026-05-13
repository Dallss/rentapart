from accounts.models import MANAGE_LEASES_PERMISSION
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLeaseManagerOrReadOnly(BasePermission):
    """
    - Anyone can read (GET)
    - Only users with ``accounts.manage_leases`` can write
    - On object level: only the listing owner can edit/delete
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.has_perm(MANAGE_LEASES_PERMISSION)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not hasattr(request.user, "profile"):
            return False
        return obj.landlord == request.user.profile
