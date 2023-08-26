from django.urls import path

from . import api_endpoints as views

app_name = 'constructor'

urlpatterns = [
    path('product_create/', views.CustomProductCreateAPIView.as_view(), name='product_create'),
    path('parts_list/', views.PartListAPIView.as_view(), name='parts_list'),
    path('models_list/', views.CustomProductModelListAPIView.as_view(), name='models_list')
]
