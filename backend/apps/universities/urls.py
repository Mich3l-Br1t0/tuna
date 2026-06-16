from django.urls import path

from apps.universities.apis import AthleteDetailApi, AthleteListCreateApi

app_name = "universities"

urlpatterns = [
    path("athletes/", AthleteListCreateApi.as_view(), name="athlete-list-create"),
    path("athletes/<int:athlete_id>/", AthleteDetailApi.as_view(), name="athlete-detail"),
]
