from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Order, OrderItem, PaymentType


class OrderItemInOrder(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'phone_number']
    list_display_links = ['id', 'status', 'phone_number']
    inlines = [OrderItemInOrder]


admin.site.register(PaymentType, TranslationAdmin)
