from django.urls import path

from . import api_endpoints as views

app_name = 'cart'

urlpatterns = [
    path('add_card_item/', views.CartItemCreateAPIView.as_view(), name='cart_item_create'),
    path('cart_items/', views.CartItemListAPIView.as_view(), name='cart_item_list'),
    path('cart_items_delete/<int:pk>/', views.CartItemDeleteAPIView.as_view(), name='cart_item_delete'),
    path('cart_items_update/<int:pk>/', views.CartItemUpdateAPIView.as_view(), name='cart_item_update'),
]
