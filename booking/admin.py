from django.contrib import admin
from .models import User, Listings, Bookings, Reviews, Property


class ListingsInline(admin.TabularInline):
    model = Listings
    extra = 1
    fields = ('active',)

class ReviewsInline(admin.TabularInline):
    model = Reviews
    extra = 1
    fields = ('rating', 'comment')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('role', 'first_name', 'last_name', 'email', 'date_joined')
    list_filter = ('role',)
    search_fields = ('last_name', 'email')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title','owner', 'city', 'location', 'price', 'property_type', 'rooms', 'created_at')
    list_filter = ('property_type', 'city', 'price')
    search_fields = ('title', 'city', 'location')
    inlines = [ListingsInline, ReviewsInline]
    ordering = ('-created_at',)




@admin.register(Listings)
class ListingsAdmin(admin.ModelAdmin):
    list_display = ('property', 'active', 'created_at')
    list_filter = ('active', 'property__property_type')
    search_fields = ('property__title', 'property__city', 'property__property_type')
    ordering = ('-created_at',)

@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'status', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'start_date')
    search_fields = ('user__username', 'listing__property__title')
    ordering = ('-created_at',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('property__title', 'user__username')
    ordering = ('-created_at',)




