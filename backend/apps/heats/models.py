from django.db import models

from apps.common.models import TimeStampedModel


class Heat(TimeStampedModel):
    stage = models.ForeignKey(
        "stages.Stage", on_delete=models.CASCADE, related_name="heats"
    )
    event = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, related_name="heats"
    )
    number = models.PositiveIntegerField()


class HeatLane(TimeStampedModel):
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE, related_name="lanes")
    athlete_registration = models.ForeignKey(
        "registrations.AthleteRegister",
        on_delete=models.CASCADE,
        related_name="heat_lanes",
    )
    number = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["heat", "number"], name="unique_lane_per_heat"
            )
        ]
