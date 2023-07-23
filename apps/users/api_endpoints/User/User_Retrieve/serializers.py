from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserRetrieveSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email']
