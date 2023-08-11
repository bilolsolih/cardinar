from .models import User
from django.db.models import Q


class PhoneNumberAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(phone_number=username) | Q(email__iexact=username), is_active=True)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None