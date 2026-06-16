"""URL configuration for the Tuna backend."""

from django.conf import settings
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
    # Domain API (athlete management, scoped to the logged-in university).
    path("api/", include("apps.universities.urls")),
]

# OpenAPI schema + browsable docs — only where API_DOCS_ENABLED (local/test, not prod).
if settings.API_DOCS_ENABLED:
    urlpatterns += [
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
