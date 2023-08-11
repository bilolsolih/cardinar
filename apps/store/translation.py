from modeltranslation.translator import TranslationOptions, translator

from .models.product import CarCover, Polik, Nakidka
from .models.product_parameters import BuildingMaterial


class CarCoverTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(CarCover, CarCoverTranslationOptions)


class PolikTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Polik, PolikTranslationOptions)


class NakidkaTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Nakidka, NakidkaTranslationOptions)


class BuildingMaterialTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(BuildingMaterial, BuildingMaterialTranslationOptions)
