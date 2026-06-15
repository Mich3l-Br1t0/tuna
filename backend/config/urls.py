"""URL configuration for the Tuna backend."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Auth: login/logout/user, password reset/confirm/change, JWT refresh/verify.
    # dj-rest-auth owns these views (accepted exception to the apis/services layering).
    path("api/auth/", include("dj_rest_auth.urls")),
    # OpenAPI schema + browsable docs (serve as the contract for the React frontend).
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
