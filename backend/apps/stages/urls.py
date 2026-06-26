from django.urls import path

from .apis import StageListApi, StageNextApi

urlpatterns = [
    path("", StageListApi.as_view(), name="stage-list"),
    path("next/", StageNextApi.as_view(), name="stage-next"),
]
