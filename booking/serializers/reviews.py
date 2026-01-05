from rest_framework import serializers
from django.utils import timezone
from django.db.models import Q

from booking.models import Reviews, Property, Bookings
from booking.serializers.user import UserShortSerializer
from booking.serializers.property import PropertyShortSerializer


class ReviewCreateSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    property = PropertyShortSerializer(read_only=True)

    property_id = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(),
                                                     write_only=True,
                                                     source='property')

    class Meta:
        model = Reviews
        fields =  ('id',
            'property',
            'property_id',
            'user',
            'rating',
            'comment',
            'created_at')
        read_only_fields = ('id', 'created_at')

    def validate(self, data):
        user = self.context['request'].user
        property_obj = data['property']


        if user.role != 'guest':
            raise serializers.ValidationError('Only guests can leave reviews.')

        has_completed_booking = Bookings.objects.filter(
            user=user,
            listing__property=property_obj
        ).filter(
            Q(status='completed') | Q(end_date__lt=timezone.now().date())
        ).exists()

        if not has_completed_booking:
            raise serializers.ValidationError('You must complete a booking before leaving a review.')

        # Проверка, что отзыв ещё не оставлен
        if Reviews.objects.filter(user=user, property=property_obj).exists():
            raise serializers.ValidationError('You already left a review.')

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReviewListSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    property = PropertyShortSerializer(read_only=True)
    class Meta:
        model = Reviews
        fields = ('id',
            'rating',
            'comment',
            'created_at',
            'user',
            'property',)
