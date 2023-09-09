from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .schema import swagger_patterns
from apps.payment.api_endpoints import payme

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('api/v1/users/', include('apps.users.urls', namespace='users')),
    path('api/v1/about/', include('apps.about.urls', namespace='about')),
    path('api/v1/cart/', include('apps.cart.urls', namespace='cart')),
    path('api/v1/store/', include('apps.store.urls', namespace='store')),
    path('api/v1/inquiries/', include('apps.inquiries.urls', namespace='inquiries')),
    path('api/v1/orders/', include('apps.orders.urls', namespace='orders')),
    path('api/v1/constructor/', include('apps.constructor.urls', namespace='constructor')),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/v1/payments/verify/', payme.PaymeAPIView.as_view(), name='payme'),
)

urlpatterns += swagger_patterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
