from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserChangePasswordSerializer


class UserChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=UserChangePasswordSerializer)
    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            if not user.check_password(old_password):
                return Response({"error": "Joriy parol noto'g'ri"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"message": "Parol o'zgartirildi"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = ['UserChangePasswordAPIView']
