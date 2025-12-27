from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import  Avg

from booking.filters import ListingsFilter
from booking.models import Listings
from booking.serializers.listings import ListingCreateSerializer, ListingSerializer
from booking.permissions import IsHostOrLandlord


class ListingsCreateView(generics.CreateAPIView):
    serializer_class = ListingCreateSerializer
    permission_classes = [IsAuthenticated, IsHostOrLandlord]

    def get_queryset(self):
        return Listings.objects.filter(property__owner=self.request.user)

class ListingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listings.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsHostOrLandlord]


class PublishedListingsView(generics.ListAPIView):
    queryset = Listings.objects.filter(active=True).select_related('property')
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ListingsFilter

    search_fields = ('property__title', 'property__city', 'property__description')
    ordering_fields = ('created_at', 'property__price','avg_rating')
    ordering = ('-avg_rating', '-created_at')


    def get_queryset(self):
        return super().get_queryset().annotate(avg_rating=Avg('property__reviews__rating'))


