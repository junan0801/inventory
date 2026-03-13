from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/login/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),

    path('api/users/', include('apps.users.urls')),
    path('api/', include('apps.goods.urls')),
    path('api/', include('apps.warehouse.urls')),
    path('api/', include('apps.inventory.urls')),
    path('api/', include('apps.inbound.urls')),
    path('api/', include('apps.outbound.urls')),
]
