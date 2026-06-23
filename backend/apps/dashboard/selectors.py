from apps.athletes.models import Athlete
from apps.registrations.models import AthleteRegister
from apps.universities.models import University


def dashboard_stats(*, university: University | None) -> dict[str, int]:
    # Scoped to the caller's faculty, to match the (scoped) athlete roster.
    athletes = Athlete.objects.filter(university=university)
    registrations = AthleteRegister.objects.filter(athlete__university=university)

    return {
        "athletes": athletes.count(),
        "registrations": registrations.count(),
        "universities": University.objects.count(),
    }
