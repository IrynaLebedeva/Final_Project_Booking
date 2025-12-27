from django.urls import path, re_path
from booking.views.listings import (ListingsCreateView,
                                    PublishedListingsView,
                                    ListingsDetailView,
                                   )



urlpatterns = [
    path('', ListingsCreateView.as_view(), name='listing-create'),
    path('all/', PublishedListingsView.as_view(), name='listing-list'),
    path('<int:pk>/', ListingsDetailView.as_view(), name='listing-detail'),

]