from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
