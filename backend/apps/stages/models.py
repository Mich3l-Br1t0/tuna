from django.db import models

from apps.common.models import TimeStampedModel


class Location(TimeStampedModel):
    address = models.CharField(max_length=255)
    lanes = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.address


class Stage(TimeStampedModel):
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name="stages",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) -> str:
        return self.name


class StageMedia(TimeStampedModel):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="media")
    drive_url = models.URLField()


class Rules(TimeStampedModel):
    version = models.PositiveIntegerField()
    file_key = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "rules"

    def __str__(self) -> str:
        return f"Rules v{self.version}"
