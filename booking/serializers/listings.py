from rest_framework import serializers

from booking.models import Listings, Property
from booking.serializers.property import PropertySerializer, PropertyShortSerializer
from booking.utils import is_listing_available


class ListingCreateSerializer(serializers.ModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(),
        source='property'
    )

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Listings
        fields = ('id', 'property_id', 'user', 'active', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate(self, data):
        user = self.context['request'].user
        property_obj = data['property']

        # host and landlord могут создавать Listing
        if user.role not in ['host', 'landlord']:
            raise serializers.ValidationError("Only host or Landlord can create listings.")

        # landlord может создавать Listing на свое жидье
        if user.role == "landlord" and property_obj.owner != user:
            raise serializers.ValidationError("Landlord can create listing only for own property")

        # для 1 жилья 1 обьявление
        if Listings.objects.filter(property=property_obj, active=True).exists():
            raise serializers.ValidationError("This property already has an active listing")

        return data




class ListingSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()
    avg_rating = serializers.FloatField(read_only=True, default=0)
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(),
                                                     write_only=True,
                                                     source='property')

    class Meta:
        model = Listings
        fields = ('id', 'property', 'property_id', 'user','active', 'available','created_at', 'avg_rating')
        read_only_fields = ('id', 'created_at')

    def get_available(self, obj):
        request = self.context['request']
        start = request.query_params.get('start_date')
        end = request.query_params.get('end_date')

        if not start or not end:
            return None


        return is_listing_available(obj, start, end)


class ListingShortSerializer(serializers.ModelSerializer):
    property = PropertyShortSerializer(read_only=True)
    class Meta:
        model = Listings
        fields = ('id', 'property', 'active')

