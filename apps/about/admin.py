from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Email, Address, PhoneNumber, SocialMedia, Banner


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()
    return None


delete_selected.short_description = _('Delete selected Banners')


class BannerTranslationAdmin(TranslationAdmin):
    actions = [delete_selected]


admin.site.register(Address, TranslationAdmin)
admin.site.register(Email)
admin.site.register(PhoneNumber)
admin.site.register(SocialMedia)
admin.site.register(Banner, BannerTranslationAdmin)
