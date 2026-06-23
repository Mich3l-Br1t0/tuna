from django.urls import path

from .apis import SiteContentDetailApi

urlpatterns = [
    path("", SiteContentDetailApi.as_view(), name="site-content"),
]
