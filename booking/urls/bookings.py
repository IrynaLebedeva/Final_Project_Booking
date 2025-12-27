from django.urls import path, re_path
from booking.views.booking import BookingCreateView, BookingListView, BookingDetailView



urlpatterns = [
    path('', BookingCreateView.as_view(), name='booking-create'),
    path('all/', BookingListView.as_view(), name='booking-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail' ),
]