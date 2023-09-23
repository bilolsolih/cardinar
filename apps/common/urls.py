from django.urls import path

from . import api_endpoints as views

app_name = 'common'

urlpatterns = [
    path('csrf_get/', views.CSRFRetrieveAPIView.as_view(), name='csrf_retrieve')
]
