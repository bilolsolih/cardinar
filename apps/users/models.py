from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name=_('Username'), max_length=128, unique=True)
    phone_number = PhoneNumberField(verbose_name=_('Phone number'), region='UZ', unique=True)
    first_name = models.CharField(verbose_name=_('First name'), max_length=128)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=128)
    email = models.EmailField(verbose_name=_('Email'), unique=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    is_staff = models.BooleanField(verbose_name=_("Staff status"), default=False)

    date_joined = models.DateTimeField(verbose_name=_("Date joined"), default=timezone.now)

    USERNAME_FIELD = 'username'

    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'email']

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username


class TelegramUser(models.Model):
    full_name = models.CharField(verbose_name=_('Full name'), max_length=128)
    chat_id = models.CharField(verbose_name=_('Chat id'), max_length=64)
    active = models.BooleanField(verbose_name=_('Can receive?'), default=True)

    class Meta:
        verbose_name = _('Telegram user')
        verbose_name_plural = _('Telegram users')

    def __str__(self):
        return f'{self.full_name} - {self.chat_id}'


class UserToken(TimeStampedModel):
    user = models.OneToOneField(verbose_name=_('User'), to='users.User', related_name='token', on_delete=models.CASCADE)
    token = models.CharField(verbose_name=_('Token'), max_length=128)

    @property
    def is_expired(self):
        return (timezone.now() - self.created) > timedelta(hours=2)

    class Meta:
        verbose_name = _('User token')
        verbose_name_plural = _('User tokens')

    def __str__(self):
        return f"Token for {self.user.username}"

# TODO: user password change - edit
