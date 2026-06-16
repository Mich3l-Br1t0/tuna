from django.db import models

from apps.common.models import TimeStampedModel


class University(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "universities"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Athlete(TimeStampedModel):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="athletes",
    )
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
