from typing import Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.universities.filters import AthleteFilter
from apps.universities.models import Athlete, University


def athlete_list(
    *, university: University, filters: dict[str, Any] | None = None
) -> QuerySet[Athlete]:
    filters = filters or {}
    qs = Athlete.objects.filter(university=university)
    return AthleteFilter(filters, queryset=qs).qs


def athlete_get(*, university: University, athlete_id: int) -> Athlete:
    return get_object_or_404(Athlete, id=athlete_id, university=university)
