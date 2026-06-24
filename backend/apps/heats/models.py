from django.db import models

from apps.common.models import TimeStampedModel


class Heat(TimeStampedModel):
    stage = models.ForeignKey(
        "stages.Stage",
        on_delete=models.CASCADE,
        related_name="heats",
        verbose_name="etapa",
    )
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="heats",
        verbose_name="prova",
    )
    number = models.PositiveIntegerField("número")


class HeatLane(TimeStampedModel):
    heat = models.ForeignKey(
        Heat, on_delete=models.CASCADE, related_name="lanes", verbose_name="bateria"
    )
    athlete_registration = models.ForeignKey(
        "registrations.AthleteRegister",
        on_delete=models.CASCADE,
        related_name="heat_lanes",
        verbose_name="inscrição do atleta",
    )
    number = models.PositiveIntegerField("raia")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["heat", "number"], name="unique_lane_per_heat"
            )
        ]
