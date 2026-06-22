from django.db import models

from apps.common.models import TimeStampedModel


class StageRegister(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        SUBMITTED = "Submitted", "Submitted"
        CONFIRMED = "Confirmed", "Confirmed"

    university = models.ForeignKey(
        "universities.University",
        on_delete=models.PROTECT,
        related_name="stage_registrations",
    )
    stage = models.ForeignKey(
        "stages.Stage", on_delete=models.CASCADE, related_name="registrations"
    )
    status = models.CharField(
        max_length=9, choices=Status.choices, default=Status.PENDING
    )
    payment_proof_key = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["university", "stage"], name="unique_university_per_stage"
            )
        ]


class AthleteRegister(TimeStampedModel):
    stage = models.ForeignKey(
        "stages.Stage", on_delete=models.CASCADE, related_name="athlete_registrations"
    )
    event = models.ForeignKey(
        "events.Event", on_delete=models.PROTECT, related_name="athlete_registrations"
    )
    athlete = models.ForeignKey(
        "athletes.Athlete", on_delete=models.PROTECT, related_name="registrations"
    )
