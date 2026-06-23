from django.urls import path

from .apis import DashboardStatsApi

urlpatterns = [
    path("stats/", DashboardStatsApi.as_view(), name="dashboard-stats"),
]
