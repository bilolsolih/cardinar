import logging
import os

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_protect

from apps.users.models import User, UserToken
from apps.users.tasks import send_email
from .serializers import UserResetPasswordSendLinkSerializer, UserResetPasswordSerializer


class UserPasswordResetSendLinkAPIView(APIView):
    serializer_class = UserResetPasswordSendLinkSerializer

    @swagger_auto_schema(request_body=UserResetPasswordSendLinkSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User with this email doesn\'t exist.'}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        user.tokens.all().delete()
        user.tokens.create(token=token)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # reset_url = request.build_absolute_uri(reverse('users:password_reset', kwargs={'uidb64': uid, 'token': token}))
        reset_url = f"http://cardinar.uz/users/reset_password/reset/{uid}/{token}/"
        send_email(
            subject='Password Reset',
            message=f'Click the link to reset your password: {reset_url}',
            sender=os.getenv('SMTP_USERNAME'),
            recipients=[email]
        )
        return Response(status=status.HTTP_200_OK)


class UserPasswordResetAPIView(APIView):
    serializer_class = UserResetPasswordSerializer

    @csrf_protect
    @swagger_auto_schema(request_body=UserResetPasswordSerializer)
    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password1 = serializer.validated_data['password1']
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token_in_database = user.tokens.last()
        if token_in_database and not token_in_database.is_expired and default_token_generator.check_token(user, token):
            user.set_password(password1)
            user.save()
            token_in_database.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'The token does not exist or has expired.'}, status.HTTP_404_NOT_FOUND)


__all__ = ['UserPasswordResetSendLinkAPIView', 'UserPasswordResetAPIView']
