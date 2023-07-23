from modeltranslation.translator import TranslationOptions, translator

from .models.product import CarCover, Polik, Nakidka


class CarCoverTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(CarCover, CarCoverTranslationOptions)


class PolikTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Polik, PolikTranslationOptions)


class NakidkaTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Nakidka, NakidkaTranslationOptions)
