from modeltranslation.translator import TranslationOptions, translator

from .models import PaymentType


class PaymentTypeTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(PaymentType, PaymentTypeTranslationOptions)
