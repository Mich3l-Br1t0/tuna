from django.urls import path

from .apis import EventListApi

urlpatterns = [
    path("", EventListApi.as_view(), name="event-list"),
]
