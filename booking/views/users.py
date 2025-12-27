from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from booking.serializers.user import RegisterSerializer


class RegisterUserView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]