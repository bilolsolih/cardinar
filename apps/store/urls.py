from django.urls import path

from . import api_endpoints as views

app_name = 'store'

urlpatterns = [
    path('products/list/', views.ProductListAPIView.as_view(), name='product_list'),
    path('products/retrieve/<int:pk>/', views.ProductRetrieveAPIView.as_view(), name='product_retrieve'),

    path('colors/list/', views.ColorListAPIView.as_view(), name='color_list'),
    path('categories/list/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('car_brands/list/', views.CarBrandListAPIView.as_view(), name='car_brand_list'),
    path('car_models/list/', views.CarModelListAPIView.as_view(), name='car_model_list'),
]
