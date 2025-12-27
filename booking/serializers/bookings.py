from rest_framework import serializers

from booking.models import Bookings, Listings
from booking.serializers.user import UserShortSerializer
from booking.serializers.listings import ListingShortSerializer
from booking.utils import is_listing_available


class BookingCreateSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    listing = ListingShortSerializer(read_only=True)

    listing_id = serializers.PrimaryKeyRelatedField(queryset=Listings.objects.all(),
                                                    write_only=True,
                                                    source='listing')

    class Meta:
        model = Bookings
        fields = ('id', 'user', 'listing', 'listing_id', 'start_date', 'end_date', 'status', 'created_at')
        read_only_fields = ('id', 'created_at', 'status')

    def validate(self, data):
        request = self.context['request']
        user = request.user

        start = data.get('start_date')
        end = data.get('end_date')
        listing = data.get('listing')

        if user.role != 'guest':   #  permissions
            raise serializers.ValidationError('Only guests can create bookings.')
        if listing.property.owner == user:   #  permissions
            raise serializers.ValidationError('You cannot book your own property.')

        if start and end and start > end:
            raise serializers.ValidationError('Start date must be before end date.')

        if not is_listing_available(listing, start, end):
            raise serializers.ValidationError(
                'This listing is not available for the selected dates.'
            )
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BookingListSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    listing = ListingShortSerializer(read_only=True)
    class Meta:
        model = Bookings
        exclude = ('id', )
