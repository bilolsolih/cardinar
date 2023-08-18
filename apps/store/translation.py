from modeltranslation.translator import TranslationOptions, translator

from .models.product import Product, Category
from .models.product_parameters import BuildingMaterial


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class BuildingMaterialTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(BuildingMaterial, BuildingMaterialTranslationOptions)
