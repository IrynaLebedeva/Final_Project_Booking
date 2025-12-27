from django.utils import timezone
from booking.models import Bookings

def is_listing_available(listing, start, end):

    if not listing.active:
        return False

    overlapping = Bookings.objects.filter(
        listing=listing,
        status__in=['pending', 'confirmed'],
        start_date__lt=end,
        end_date__gt=start
    ).exists()

    return not overlapping