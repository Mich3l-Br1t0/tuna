from apps.universities.models import University

from .models import Athlete


def athlete_create(*, name: str, gender: str, university: University) -> Athlete:
    return Athlete.objects.create(name=name, gender=gender, university=university)


def athlete_update(*, athlete: Athlete, name: str, gender: str) -> Athlete:
    athlete.name = name
    athlete.gender = gender
    athlete.save()
    return athlete


def athlete_delete(*, athlete: Athlete) -> None:
    athlete.delete()
