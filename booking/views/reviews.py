from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from booking.models import Reviews
from booking.serializers.reviews import ReviewCreateSerializer, ReviewListSerializer
from booking.permissions import IsGuest, IsReviewOwner


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsGuest]


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return Reviews.objects.filter(property_id=property_id)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]

