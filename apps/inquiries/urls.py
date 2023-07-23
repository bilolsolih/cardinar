from django.urls import path

from . import api_endpoints as views

app_name = 'inquiries'

urlpatterns = [
    path('inquiry/', views.InquiryCreateAPIView.as_view(), name='inquiry_create'),
]
