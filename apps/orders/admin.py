from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInOrder(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'delivery_type', 'is_paid', 'is_canceled', 'final_price']
    list_display_links = ['id', 'full_name', 'phone_number']
    list_filter = ['delivery_type', 'is_paid', 'is_canceled']
    inlines = [OrderItemInOrder]
