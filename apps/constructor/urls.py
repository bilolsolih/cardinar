from django.urls import path
from . import api_endpoints as views

app_name = 'constructor'

urlpatterns = [
    path('car_cover/', views.ConstructedProductCreateAPIView.as_view(), name='car-cover'),
]
