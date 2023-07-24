from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Inquiry


def mark_dealt_with(modeladmin, request, queryset):
    for obj in queryset:
        obj.active = False
        obj.save()
    return None


mark_dealt_with.short_description = _('Mark the chosen Inquiries as dealt with.')


class InquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'email', 'active']
    list_editable = ['active']
    list_filter = ['active']
    actions = [mark_dealt_with]


admin.site.register(Inquiry, InquiryAdmin)
