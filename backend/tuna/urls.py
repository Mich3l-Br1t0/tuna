from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/site-content/", include("apps.site_content.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),
    path("api/athletes/", include("apps.athletes.urls")),
    path("api/events/", include("apps.events.urls")),
    path("api/stages/", include("apps.stages.urls")),
    path("api/registrations/", include("apps.registrations.urls")),
]
