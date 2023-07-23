from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Order, OrderItem, PaymentType

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentType, TranslationAdmin)
