from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, TelegramUser, UserToken


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    readonly_fields = ['last_login', 'date_joined']
    ordering = ('username',)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'chat_id', 'active']
    list_editable = ['active']
    list_filter = ['active']
    search_fields = ['full_name', 'chat_id']


admin.site.register(User, CustomUserAdmin)


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_expired']
    readonly_fields = ['is_expired']


admin.site.register(UserToken, UserTokenAdmin)
# Register your models here.
