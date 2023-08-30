from django.urls import path

from .api_endpoints import payme

app_name = "payments"

urlpatterns = [
    path("verify/", payme.PaymeAPIView.as_view(), name="payme"),
]
