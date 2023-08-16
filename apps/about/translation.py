from modeltranslation.translator import translator, TranslationOptions

from .models import Address, Banner


class BannerTranslationOptions(TranslationOptions):
    fields = ('text',)


translator.register(Banner, BannerTranslationOptions)


class AddressTranslationOptions(TranslationOptions):
    fields = ('region', 'district', 'street')


translator.register(Address, AddressTranslationOptions)
