from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Order, OrderItem, PaymentType


class OrderItemInOrder(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'delivery_type', 'is_paid', 'is_canceled', 'final_price']
    list_display_links = ['id', 'full_name', 'phone_number']
    list_filter = ['delivery_type', 'is_paid', 'is_canceled']
    inlines = [OrderItemInOrder]


admin.site.register(PaymentType, TranslationAdmin)
