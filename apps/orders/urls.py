from django.urls import path

from . import api_endpoints as views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateAPIView.as_view(), name='order_create'),
    path('list/', views.OrderListAPIView.as_view(), name='order_list'),
    path('retrieve/<int:pk>/', views.OrderRetrieveAPIView.as_view(), name='order_retrieve'),
]
