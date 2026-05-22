from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBookerOrReadOnly(BasePermission):
   """
   - Any authenticated user can create bookings
   - Only booking owner can edit/delete their booking
   """

   def has_permission(self, request, view):
      if request.method in SAFE_METHODS:
         return True
      return request.user and request.user.is_authenticated

   def has_object_permission(self, request, view, obj):
      if request.method in SAFE_METHODS:
         return True
      return obj.booker == request.user