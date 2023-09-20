from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models.product import Category, Product, Photo, PremiumPhoto, Articul
from .models.product_parameters import Color, CarModel, CarBrand, BuildingMaterial
from .models.store import Store


def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        for photo in obj.photos.all():
            photo.delete()
        obj.delete()
    return None


delete_selected.short_description = 'Delete selected objects'


class ArticulInProduct(admin.TabularInline):
    model = Articul


class PhotoInProduct(admin.TabularInline):
    model = Photo


class PremiumPhotoInProduct(admin.TabularInline):
    model = PremiumPhoto


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'category', 'price', 'status', 'no_in_stock', 'active']
    list_display_links = ['id', 'title', 'category']
    list_editable = ['price', 'status', 'no_in_stock', 'active']
    actions = [delete_selected]
    inlines = [ArticulInProduct, PhotoInProduct, PremiumPhotoInProduct]


admin.site.register(BuildingMaterial, TranslationAdmin)
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(Category, TranslationAdmin)
admin.site.register(Color)
admin.site.register(Store)
