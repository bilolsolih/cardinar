from modeltranslation.translator import translator, TranslationOptions

from .models import Address, Banner


class BannerTranslationOptions(TranslationOptions):
    fields = ('text',)


class AddressTranslationOptions(TranslationOptions):
    fields = ('region', 'district', 'street')


translator.register(Banner, BannerTranslationOptions)
translator.register(Address, AddressTranslationOptions)
