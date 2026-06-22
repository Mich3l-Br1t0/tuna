from django.db import models

from apps.common.models import TimeStampedModel


class Result(TimeStampedModel):
    class Status(models.TextChoices):
        COMPLETED = "Completed", "Completed"
        DNF = "DNF", "Did Not Finish"
        DNS = "DNS", "Did Not Start"
        DQ = "DQ", "Disqualified"

    # Exactly one of these is set (enforced by the check constraint below).
    athlete_register = models.ForeignKey(
        "registrations.AthleteRegister",
        on_delete=models.CASCADE,
        related_name="results",
        null=True,
        blank=True,
    )
    relay_entry = models.ForeignKey(
        "athletes.RelayEntry",
        on_delete=models.CASCADE,
        related_name="results",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=9, choices=Status.choices)
    position = models.PositiveIntegerField()
    result = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    is_record = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(athlete_register__isnull=False, relay_entry__isnull=True)
                    | models.Q(athlete_register__isnull=True, relay_entry__isnull=False)
                ),
                name="result_exactly_one_entry",
            )
        ]
