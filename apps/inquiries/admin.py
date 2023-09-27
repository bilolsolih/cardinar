from django.contrib import admin

from .models import Inquiry, InquiryCall, InquiryOneClick


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'on_product', 'articul', 'active']
    list_display_links = ['id', 'full_name', 'phone_number']
    list_editable = ['active']

    def get_queryset(self, request):
        qs = self.model._default_manager.filter(is_product=True)
        ordering = self.get_ordering(request)
        if ordering:
            qs.order_by(*ordering)
        return qs


@admin.register(InquiryCall)
class InquiryCallAdmin(InquiryAdmin):
    def get_queryset(self, request):
        qs = self.model._default_manager.filter(is_call=True)
        ordering = self.get_ordering(request)
        if ordering:
            qs.order_by(*ordering)
        return qs


@admin.register(InquiryOneClick)
class InquiryOneClickAdmin(InquiryAdmin):
    def get_queryset(self, request):
        qs = self.model._default_manager.filter(is_one_click=True)
        ordering = self.get_ordering(request)
        if ordering:
            qs.order_by(*ordering)
        return qs
