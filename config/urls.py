
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT
    path("api/auth/token/", TokenObtainPairView.as_view(),name="token_obtain_pair" ),
    path("api/auth/token/refresh/",TokenRefreshView.as_view(), name="token_refresh"),

    # Accounts App
    path("api/auth/", include("apps.accounts.api.urls")),

    # CMS
    path( "api/cms/",include("apps.cms.api.urls")),

    # Public
    path("api/public/", include("apps.public_api.api.urls")),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )