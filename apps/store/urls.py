from django.urls import path

from . import api_endpoints as views

app_name = 'store'

urlpatterns = [
    path('car_covers/list/', views.CarCoverListAPIView.as_view(), name='car_cover_list'),
    path('car_covers/retrieve/<int:pk>/', views.CarCoverRetrieveAPIView.as_view(), name='car_cover_retrieve'),
    path('nakidkas/list/', views.NakidkaListAPIView.as_view(), name='nakidka_list'),
    path('nakidkas/retrieve/<int:pk>/', views.NakidkaRetrieveAPIView.as_view(), name='nakidka_retrieve'),
    path('poliks/list/', views.PolikListAPIView.as_view(), name='polik_list'),
    path('poliks/retrieve/<int:pk>/', views.PolikRetrieveAPIView.as_view(), name='polik_retrieve'),

    path('colors/list/', views.ColorListAPIView.as_view(), name='color_list'),
    path('categories/list/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('car_brands/list/', views.CarBrandListAPIView.as_view(), name='car_brand_list'),
    path('car_models/list/<int:brand_id>/', views.CarModelListAPIView.as_view(), name='car_model_list'),
]
