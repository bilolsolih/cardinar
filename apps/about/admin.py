from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Email, Address, PhoneNumber, SocialMedia, Banner


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()
    return None


delete_selected.short_description = _('Delete selected Banners')


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
    list_display = ['id', 'photo', 'text']
    list_display_links = ['id']
    list_editable = ['photo', 'text']

    actions = [delete_selected]


@admin.register(Address)
class AddressAdmin(TranslationAdmin):
    list_display = ['id', 'region', 'district', 'street', 'house_no']
    list_display_links = ['id']
    list_editable = ['region', 'district', 'street', 'house_no']
    search_fields = ['region', 'district', 'street', 'house_no']


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    list_display_links = ['id']
    list_editable = ['email']


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number']
    list_display_links = ['id']
    list_editable = ['phone_number']


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'social_media', 'link']
    list_display_links = ['id', 'social_media']
    list_editable = ['link']
