from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CSRFRetrieveAPIView(APIView):
    def get(self, request, *args, **kwargs):
        token = get_token(request)
        return Response({"token": token}, status=status.HTTP_200_OK)


__all__ = ['CSRFRetrieveAPIView']
