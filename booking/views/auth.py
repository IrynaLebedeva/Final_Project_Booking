from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            refresh = request.COOKIES.get('refresh_token')

            if refresh:
                token = RefreshToken(refresh)
                token.blacklist()

        except Exception as exc:
            return Response(
                data={
                    "message": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response