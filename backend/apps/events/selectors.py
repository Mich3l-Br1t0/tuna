from django.db.models import QuerySet

from .models import Event


def event_list() -> QuerySet[Event]:
    return Event.objects.select_related("category").order_by("name")
