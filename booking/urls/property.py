from django.urls import path, re_path
from booking.views.property import (PropertyListView,
                                    PropertyDetailView,
                                    PropertyCreateView
                                    )



urlpatterns = [
    path('', PropertyCreateView.as_view(), name='property-create'),
    path('all/', PropertyListView.as_view(), name='property-list'),
    path('<int:pk>/',PropertyDetailView.as_view(), name='property-detail'),
]