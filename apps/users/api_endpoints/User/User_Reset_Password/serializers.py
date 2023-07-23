from rest_framework import serializers


class UserResetPasswordSendLinkSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password1 = attrs['password1']
        password2 = attrs['password2']
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
        if len(password1) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return attrs
