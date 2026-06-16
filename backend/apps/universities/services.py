from apps.universities.models import Athlete, University


def athlete_create(*, university: University, name: str) -> Athlete:
    athlete = Athlete(university=university, name=name)
    athlete.full_clean()
    athlete.save()
    return athlete


def athlete_update(*, athlete: Athlete, name: str) -> Athlete:
    athlete.name = name
    athlete.full_clean()
    athlete.save()
    return athlete


def athlete_delete(*, athlete: Athlete) -> None:
    athlete.delete()
