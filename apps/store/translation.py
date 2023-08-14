from modeltranslation.translator import TranslationOptions, translator

from .models.product import Product
from .models.product_parameters import BuildingMaterial


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Product, ProductTranslationOptions)


class BuildingMaterialTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(BuildingMaterial, BuildingMaterialTranslationOptions)
