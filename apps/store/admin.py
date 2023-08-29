from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models.product import Category, Product, Photo
from .models.product_parameters import Color, CarModel, CarBrand, BuildingMaterial
from .models.store import Store


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        for photo in obj.photos.all():
            photo.delete()
        obj.delete()
    return None


delete_selected.short_description = 'Delete selected objects'


class PhotoInProduct(admin.TabularInline):
    model = Photo


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    actions = [delete_selected]
    inlines = [PhotoInProduct]


admin.site.register(BuildingMaterial, TranslationAdmin)
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(Category, TranslationAdmin)
admin.site.register(Color)
admin.site.register(Store)
