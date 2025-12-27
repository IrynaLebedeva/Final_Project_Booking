from django.urls import path

from booking.views.users import RegisterUserView

urlpatterns = [
    path('', RegisterUserView.as_view()),
]