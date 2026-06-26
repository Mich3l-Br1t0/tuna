from apps.universities.models import University

from .models import Athlete


def athlete_create(
    *,
    name: str,
    gender: str,
    university: University,
    event_ids: list[int] | None = None,
) -> Athlete:
    athlete = Athlete.objects.create(name=name, gender=gender, university=university)
    athlete.events.set(event_ids or [])
    return athlete


def athlete_update(
    *,
    athlete: Athlete,
    name: str,
    gender: str,
    event_ids: list[int] | None = None,
) -> Athlete:
    athlete.name = name
    athlete.gender = gender
    athlete.save()
    athlete.events.set(event_ids or [])
    return athlete


def athlete_delete(*, athlete: Athlete) -> None:
    athlete.delete()
