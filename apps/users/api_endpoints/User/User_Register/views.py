from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response

from apps.cart.models import Cart, CartItem
from apps.users.models import User
from .custom_permission import IsNotRegisteredAlready
from .serializers import UserRegisterSerializer


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [IsNotRegisteredAlready]
    parser_classes = [JSONParser, FormParser]

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('device_id', openapi.IN_QUERY, description='Device id', type=openapi.TYPE_STRING), ])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        cd = dict(serializer.validated_data)
        defaults = dict()
        username = cd['username']
        for key, value in cd.items():
            if key in ('username', 'password1', 'password2'):
                continue
            else:
                defaults[key] = value

        if User.objects.filter(username=username, is_active=True).first():
            return Response({'message': 'Username is not available.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.get(username=username, is_active=False)
                for key, value in defaults.items():
                    setattr(user, key, value)
                user.is_active = True
            except User.DoesNotExist:
                user = User.objects.create(username=username, **defaults)

            user.set_password(cd['password1'])
            user.save()
            Cart.objects.create(user=user)
            device_id = self.request.query_params.get('device_id', None)
            if device_id and CartItem.objects.filter(device_id=device_id).exists():
                CartItem.objects.filter(device_id=device_id).update(cart=user.cart)
            return Response(status=status.HTTP_201_CREATED)


__all__ = ['UserRegisterAPIView']
