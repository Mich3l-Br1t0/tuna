from django.urls import path

from .apis import (
    AthleteCreateApi,
    AthleteDeleteApi,
    AthleteListApi,
    AthleteUpdateApi,
)

urlpatterns = [
    path("", AthleteListApi.as_view(), name="athlete-list"),
    path("create/", AthleteCreateApi.as_view(), name="athlete-create"),
    path("<int:athlete_id>/update/", AthleteUpdateApi.as_view(), name="athlete-update"),
    path("<int:athlete_id>/delete/", AthleteDeleteApi.as_view(), name="athlete-delete"),
]
