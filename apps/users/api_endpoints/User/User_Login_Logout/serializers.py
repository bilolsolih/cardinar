from django.contrib.auth import authenticate
from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise serializers.ValidationError('Invalid username or password.')
        attrs['user'] = user
        return attrs
