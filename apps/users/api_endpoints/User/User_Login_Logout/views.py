from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .custom_permissions import IsNotAuthenticated
from .serializers import UserLoginSerializer


class UserLoginAPIView(APIView):
    permission_classes = [IsNotAuthenticated]

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        else:
            pass
        return Response(status=status.HTTP_200_OK)


__all__ = ['UserLoginAPIView', 'UserLogoutAPIView']
