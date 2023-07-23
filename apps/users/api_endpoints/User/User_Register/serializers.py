from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField

from apps.users.models import User


class UserRegisterSerializer(ModelSerializer):
    password1 = CharField(min_length=8, max_length=32)
    password2 = CharField(min_length=8, max_length=32)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2']
        extra_kwargs = {
            'username': {'validators': []},
        }

    def validate(self, attrs):
        super().validate(attrs)
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({"password1": "Passwords do not math. Please try again."})
        return attrs
