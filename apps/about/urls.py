from django.urls import path

from . import api_endpoints as views

app_name = 'about'

urlpatterns = [
    path('addresses/', views.AddressListAPIView.as_view(), name='address_list'),
    path('banneres/', views.BannerListAPIView.as_view(), name='banner_list'),
    path('emails/', views.EmailListAPIView.as_view(), name='email_list'),
    path('phone_numbers/', views.PhoneNumberListView.as_view(), name='phone_number_list'),
    path('social_medias/', views.SocialMediaListAPIView.as_view(), name='social_media_list')
]
