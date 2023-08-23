from django.apps import apps as a
from django.conf import settings


def populate_with(model):
    custom_apps = settings.CUSTOM_APPS
    for i, app in enumerate(custom_apps):
        custom_apps[i] = app.split('.', 1)[1]


    # for field in model._meta.fields:
    #     print("*" * 50, field.name, "*" * 50)
    #     attributes = dir(field)
    #     for attr in attributes:
    #         print(attr)


def populate(model):
    for field in model._meta.fields:
        if field.has_default:
            pass
