from django.urls import path

from .apis import (
    AthleteEntrySetApi,
    StageRegisterCreateApi,
    StageRegisterDetailApi,
)

urlpatterns = [
    path(
        "<int:stage_id>/",
        StageRegisterDetailApi.as_view(),
        name="stage-register-detail",
    ),
    path(
        "<int:stage_id>/register/",
        StageRegisterCreateApi.as_view(),
        name="stage-register-create",
    ),
    path(
        "<int:stage_id>/athletes/<int:athlete_id>/set/",
        AthleteEntrySetApi.as_view(),
        name="athlete-entry-set",
    ),
]
