from django.urls import path
from booking.views.reviews import (ReviewCreateView,
                                    ReviewListView,
                                    ReviewDetailView
                                    )



urlpatterns = [
    path('', ReviewCreateView.as_view(), name='review-create'),
    path('property/<int:property_id>/', ReviewListView.as_view(), name='review-list'),
    path('<int:pk>/',ReviewDetailView.as_view(), name='review-detail'),
]