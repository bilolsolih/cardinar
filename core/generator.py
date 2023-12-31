from django.conf import settings
from drf_yasg.generators import OpenAPISchemaGenerator


class HttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https", "http"]
        if settings.STAGE == "production":
            schema.schemes = ["https", "http"]
        return schema
