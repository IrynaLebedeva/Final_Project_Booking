from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from booking.views.users import UserLoginAPIView, RegisterUserView
from booking.views.auth import LogoutUser

router = DefaultRouter()

urlpatterns = [
    path('property/', include('booking.urls.property')),
    path('bookings/', include('booking.urls.bookings')),
    path('listings/', include('booking.urls.listings')),
    path('reviews/', include('booking.urls.reviews')),
    path('user/', include('booking.urls.user')),
    path('auth/logout/', LogoutUser.as_view(), name='logout'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]