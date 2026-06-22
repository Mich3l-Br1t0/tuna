from django.db import models

from apps.common.models import TimeStampedModel


class EventCategory(TimeStampedModel):
    class Type(models.TextChoices):
        TRACK = "Track", "Track"
        FIELD = "Field", "Field"

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=5, choices=Type.choices)

    class Meta:
        verbose_name_plural = "event categories"

    def __str__(self) -> str:
        return self.name


class Event(TimeStampedModel):
    class MeasurementType(models.TextChoices):
        SECONDS = "seconds", "Seconds"
        METERS = "meters", "Meters"

    category = models.ForeignKey(
        EventCategory, on_delete=models.PROTECT, related_name="events"
    )
    measurement_type = models.CharField(max_length=7, choices=MeasurementType.choices)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class EventData(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="data")
    stage = models.ForeignKey(
        "stages.Stage", on_delete=models.CASCADE, related_name="event_data"
    )
    start_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "event data"
