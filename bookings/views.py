from rest_framework import viewsets
from .models import Booking
from .serializers import BookingsSerializer
from .permissions import IsBookerOrReadOnly


class BookingViewSet(viewsets.ModelViewSet):
   queryset = Booking.objects.all()
   serializer_class = BookingsSerializer
   permission_classes = [IsBookerOrReadOnly]

   def perform_create(self, serializer):
      serializer.save(booker=self.request.user)