from django.db.models import QuerySet

from apps.athletes.models import Athlete
from apps.events.models import Event, EventData
from apps.stages.models import Stage
from apps.universities.models import University

from .models import AthleteRegister, StageRegister


def stage_register_get(*, university: University, stage: Stage) -> StageRegister | None:
    return StageRegister.objects.filter(university=university, stage=stage).first()


def stage_offered_provas(*, stage: Stage) -> list[dict]:
    """Provas the stage offers, each with the naipes (genders) it's offered for.
    Provas ordered by name; genders ordered M then F."""
    provas: dict[int, dict] = {}
    for row in (
        EventData.objects.filter(stage=stage)
        .values("event_id", "event__name", "gender")
        .order_by("event__name")
    ):
        prova = provas.setdefault(
            row["event_id"],
            {"id": row["event_id"], "name": row["event__name"], "genders": []},
        )
        if row["gender"] not in prova["genders"]:
            prova["genders"].append(row["gender"])
    for prova in provas.values():
        prova["genders"].sort(key=lambda g: 0 if g == "M" else 1)
    return list(provas.values())


def eligible_events_for_athlete(*, athlete: Athlete, stage: Stage) -> QuerySet[Event]:
    """Provas the athlete can do that this stage offers for the athlete's gender."""
    return Event.objects.filter(
        data__stage=stage,
        data__gender=athlete.gender,
        athletes=athlete,
    ).distinct()


def registration_athletes(*, university: University, stage: Stage) -> list[dict]:
    """The university's athletes that have at least one eligible event at the
    stage, each with their eligible events and currently-selected event ids."""
    # Events the stage offers, grouped by naipe.
    offered: dict[str, set[int]] = {}
    for ed in EventData.objects.filter(stage=stage).values("event_id", "gender"):
        offered.setdefault(ed["gender"], set()).add(ed["event_id"])

    selected_by_athlete: dict[int, list[int]] = {}
    for athlete_id, event_id in AthleteRegister.objects.filter(
        stage=stage, athlete__university=university
    ).values_list("athlete_id", "event_id"):
        selected_by_athlete.setdefault(athlete_id, []).append(event_id)

    result = []
    for athlete in Athlete.objects.filter(university=university).prefetch_related(
        "events"
    ):
        offered_ids = offered.get(athlete.gender, set())
        eligible = [e for e in athlete.events.all() if e.id in offered_ids]
        if not eligible:
            continue
        result.append(
            {
                "id": athlete.pk,
                "name": athlete.name,
                "gender": athlete.gender,
                "eligible_events": [{"id": e.id, "name": e.name} for e in eligible],
                "selected_event_ids": selected_by_athlete.get(athlete.pk, []),
            }
        )
    return result
