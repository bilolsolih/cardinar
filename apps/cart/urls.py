from django.urls import path

from . import api_endpoints as views

app_name = 'cart'

urlpatterns = [
    path('cart_items/create_update/', views.CartItemCreateUpdateAPIView.as_view(), name='cart_item_create_update'),
    path('cart_items/', views.CartItemListAPIView.as_view(), name='cart_item_list'),
    path('cart_items_delete/<int:pk>/', views.CartItemDeleteAPIView.as_view(), name='cart_item_delete'),

]
