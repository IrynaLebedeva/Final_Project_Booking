import django_filters
from booking.models import Listings


class ListingsFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(
        field_name='property__city',
        lookup_expr='iexact'
    )

    property_type = django_filters.CharFilter(
        field_name='property__property_type'
    )

    min_price = django_filters.NumberFilter(
        field_name='property__price',
        lookup_expr='gte'
    )

    max_price = django_filters.NumberFilter(
        field_name='property__price',
        lookup_expr='lte'
    )

    rooms = django_filters.NumberFilter(
        field_name='property__rooms'
    )

    class Meta:
        model = Listings
        fields = [
            'city',
            'property_type',
            'min_price',
            'max_price',
            'rooms',
        ]
