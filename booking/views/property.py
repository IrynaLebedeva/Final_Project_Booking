from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from booking.models import Property
from booking.serializers.property import PropertySerializer

from booking.permissions import  IsLandlord, IsHostOrLandlord


class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsHostOrLandlord]

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsLandlord]

class PropertyCreateView(generics.CreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsLandlord]




