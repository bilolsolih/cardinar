from django.urls import path
from . import api_endpoints as views

app_name = 'constructor'

urlpatterns = [
    path('car_cover/', views.CarCoverCreateAPIView.as_view(), name='car-cover'),
    path('nakidka_create/', views.NakidkaCreateAPIView.as_view(), name='nakidka-cover'),
    path('polik_create/', views.PolikCreateAPIView.as_view(), name='polik-cover'),
]
