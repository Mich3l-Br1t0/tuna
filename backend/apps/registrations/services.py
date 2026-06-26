from rest_framework.exceptions import ValidationError

from apps.athletes.models import Athlete
from apps.stages.models import Stage
from apps.stages.selectors import registration_is_open
from apps.universities.models import University

from .models import AthleteRegister, StageRegister
from .selectors import eligible_events_for_athlete


def _assert_open(stage: Stage) -> None:
    if not registration_is_open(stage):
        raise ValidationError("Prazo de inscrição encerrado.")


def stage_register_create(*, university: University, stage: Stage) -> StageRegister:
    _assert_open(stage)
    register, _ = StageRegister.objects.get_or_create(
        university=university, stage=stage
    )
    return register


def athlete_entry_set(
    *,
    university: University,
    stage: Stage,
    athlete: Athlete,
    event_ids: list[int],
) -> None:
    """Set the athlete's provas for this stage to exactly `event_ids`, creating
    missing entries and removing the rest."""
    _assert_open(stage)
    if athlete.university != university:
        raise ValidationError("Este atleta não pertence à sua universidade.")

    eligible_ids = set(
        eligible_events_for_athlete(athlete=athlete, stage=stage).values_list(
            "id", flat=True
        )
    )
    target_ids = set(event_ids)
    invalid = target_ids - eligible_ids
    if invalid:
        raise ValidationError("Prova inválida para este atleta nesta etapa.")

    StageRegister.objects.get_or_create(university=university, stage=stage)

    current_ids = set(
        AthleteRegister.objects.filter(stage=stage, athlete=athlete).values_list(
            "event_id", flat=True
        )
    )

    to_add = target_ids - current_ids
    to_remove = current_ids - target_ids

    AthleteRegister.objects.bulk_create(
        [
            AthleteRegister(stage=stage, athlete=athlete, event_id=event_id)
            for event_id in to_add
        ]
    )
    if to_remove:
        AthleteRegister.objects.filter(
            stage=stage, athlete=athlete, event_id__in=to_remove
        ).delete()
