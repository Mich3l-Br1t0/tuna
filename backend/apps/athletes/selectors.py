from typing import Any

from django.db.models import QuerySet

from apps.universities.models import University

from .models import Athlete


def athlete_list(
    *, university: University | None, filters: dict[str, Any] | None = None
) -> QuerySet[Athlete]:
    filters = filters or {}

    qs = (
        Athlete.objects.filter(university=university)
        .prefetch_related("events")
        .order_by("name")
    )

    if filters.get("name"):
        qs = qs.filter(name__icontains=filters["name"])
    if filters.get("gender"):
        qs = qs.filter(gender=filters["gender"])
    if filters.get("event"):
        qs = qs.filter(events=filters["event"])

    return qs
