import random
import string

from django.apps import apps
from django.conf import settings
from django.db import models
from lorem_text import lorem


def generate_string(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def generate_email():
    characters = string.ascii_letters + string.digits
    random_email = ''.join(random.choice(characters) for _ in range(1, random.randint(5, 20))) + '@' + ''.join(random.choice(characters) for _ in range(1, 4)) + '.com'
    return random_email


def populate_independent(models_list: list):
    for model in models_list:
        defaults = {}
        for field in model._meta.fields:
            if field.__class__ is not models.BigAutoField and not field.has_default() and not field.null:
                match field.__class__:
                    case models.CharField:
                        defaults[field.name] = generate_string(field.max_length)
                    case models.TextField:
                        defaults[field.name] = lorem.paragraph()
                    case models.IntegerField | models.PositiveIntegerField | models.SmallIntegerField | models.BigIntegerField | models.PositiveBigIntegerField | models.PositiveSmallIntegerField:
                        defaults[field.name] = random.randint(1, 9999)
                    case models.DecimalField | models.FloatField:
                        defaults[field.name] = random.randint(1, 9999)
                    case models.EmailField:
                        defaults[field.name] = generate_email()
        model.objects.create(**defaults)


def get_models(model=None, app=None):
    custom_apps = settings.CUSTOM_APPS
    models_list = list()
    for i, app_label in enumerate(custom_apps):
        app = apps.get_app_config(app_label=app_label.split('.', 1)[1])
        if app.models:
            for value in list(app.models.values()):
                if "_" not in value._meta.model_name:
                    models_list.append(value)

    independent_models = list()
    dependent_models = list()
    for m in models_list:
        is_dependant = False
        for field in m._meta.fields:
            if field.__class__ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
                is_dependant = True
                break
        if is_dependant:
            dependent_models.append(m)
        else:
            independent_models.append(m)

    populate_independent(independent_models)
    # now I have models separated into dependent and independent lists
# For each model, the list of models on which the model depends must be identified
# if the model has some other models on which it depends, each of those models must be checked for dependency
# and so the loop must go on.
# The first thing which crossed my mind is using recursive functions. This could be the first time I successfully implement one
