from django.contrib import admin
from .models import CustomProductModel, CustomProduct, Part

admin.site.register(CustomProductModel)
admin.site.register(CustomProduct)
admin.site.register(Part)
