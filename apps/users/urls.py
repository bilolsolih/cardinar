from django.urls import path

from . import api_endpoints as views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view(), name='user_register'),
    path('login/', views.UserLoginAPIView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='user_logout'),
    path('retrieve/', views.UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('update/', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('delete/', views.UserDeleteAPIView.as_view(), name='user_delete'),
    path('change_password/', views.UserChangePasswordAPIView.as_view(), name='change_password'),
    path('reset_password/send_link/', views.UserPasswordResetSendLinkAPIView.as_view(), name='password_reset_send'),
    path('reset_password/reset/<str:uidb64>/<str:token>/', views.UserPasswordResetAPIView.as_view(), name='password_reset'),
]
