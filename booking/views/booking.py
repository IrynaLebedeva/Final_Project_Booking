from rest_framework import generics
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.db import transaction

from booking.models import Bookings
from booking.serializers.bookings import BookingCreateSerializer, BookingListSerializer
from booking.permissions import IsGuest, IsHostOrLandlord


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated, IsGuest]


class BookingListView(ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        status_param = self.request.query_params.get('status')

        # guest — свои бронирования
        if user.role == 'guest':
            qs = Bookings.objects.filter(user=user)

        # host — бронирования его объявлений
        elif user.role == 'host':
            qs = Bookings.objects.filter(listing__user=user)

        # landlord — бронирования его недвижимости
        elif user.role == 'landlord':
            qs = Bookings.objects.filter(listing__property__owner=user)

        else:
            qs = Bookings.objects.none()

        today = now().date()

        # Авто-перевод всех истёкших бронирований в completed
        qs.filter(end_date__lt=today, status__in=['confirmed', 'pending']).update(status='completed')


    # Фильтрация по статусу
        if status_param == 'active':
            qs = qs.filter(status__in=['pending', 'confirmed'])

        elif status_param == 'completed':
            qs = qs.filter(status='completed')

        elif status_param == 'inactive':
            qs = qs.filter(status__in=['canceled', 'rejected'])

        # если передали конкретный статус
        elif status_param:
            qs = qs.filter(status=status_param)

        return qs.order_by('-created_at')


class BookingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        booking = self.get_object()
        action = request.data.get('action')
        user = request.user

        if action not in ['cancel', 'confirm', 'reject']:
            return Response({'detail': 'Invalid action.'},
                            status=status.HTTP_400_BAD_REQUEST)

         # Авто-перевод в completed, если бронирование закончилось
        if booking.end_date < now().date() and booking.status in ['confirmed', 'pending']:
            booking.status = 'completed'
            booking.save()
            serializer = self.get_serializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # CANCEL — только guest может отменять свои брони
        if action == 'cancel':
            if user.role != 'guest' or booking.user != user:
                return Response({'detail': 'Only guests can cancel their bookings.'},
                                status=status.HTTP_403_FORBIDDEN)

            if booking.start_date <= now().date():
                return Response({'detail': 'Too late to cancel booking.'},
                                status=status.HTTP_400_BAD_REQUEST)
            booking.status = 'canceled'
            booking.save()
            serializer = self.get_serializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # CONFIRM / REJECT — только host или landlord
        if action in ['confirm', 'reject']:
            if user.role not in ['host', 'landlord']:
                return Response({'detail': 'Only hosts and landlords can confirm or reject bookings.'},
                                status=status.HTTP_403_FORBIDDEN)

            # Проверяем, что пользователь действительно владелец
            if user.role == 'host' and booking.listing.user != user:
                return Response({'detail': 'You do not own this listing.'},
                                    status=status.HTTP_403_FORBIDDEN)
            if user.role == 'landlord' and booking.listing.property.owner != user:
                    return Response({'detail': 'You do not own this property.'},
                                    status=status.HTTP_403_FORBIDDEN)

            if action == 'confirm':
                overlapping = Bookings.objects.filter(
                    listing=booking.listing,
                    status__in=['pending', 'confirmed'],
                    start_date__lt=booking.end_date,
                    end_date__gt=booking.start_date
                ).exclude(pk=booking.pk)

                # overlapping.update(status='rejected')  #  не нужно, т.к. параллельное бронирование запрещено
                booking.status = 'confirmed'

            if action == 'reject':
                booking.status = 'rejected'

            booking.save()

            serializer = self.get_serializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'detail': 'Action not processed.'}, status=status.HTTP_400_BAD_REQUEST)




