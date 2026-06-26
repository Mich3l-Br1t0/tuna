from django.urls import path

from .apis import StageNextApi

urlpatterns = [
    path("next/", StageNextApi.as_view(), name="stage-next"),
]
