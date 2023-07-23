from django.contrib import admin

from .models.product import Category
from .models.product_parameters import Color
from .models.store import Store


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()
    return None


delete_selected.short_description = 'Delete selected objects'

admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Color)
