from django.contrib import admin

from .models.product import Category, CarCover, Nakidka, Polik, Photo
from .models.product_parameters import Color, CarModel, CarBrand, BuildingMaterial
from .models.store import Store


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()
    return None


delete_selected.short_description = 'Delete selected objects'

admin.site.register(BuildingMaterial)
admin.site.register(CarBrand)
admin.site.register(CarCover)
admin.site.register(CarModel)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Nakidka)
admin.site.register(Photo)
admin.site.register(Polik)
admin.site.register(Store)



