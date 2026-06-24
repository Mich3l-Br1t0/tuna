from django.db import models

from apps.common.models import TimeStampedModel


class EventCategory(TimeStampedModel):
    class Type(models.TextChoices):
        TRACK = "Track", "Pista"
        FIELD = "Field", "Campo"

    name = models.CharField("nome", max_length=255)
    type = models.CharField("tipo", max_length=5, choices=Type.choices)

    class Meta:
        verbose_name = "categoria da prova"
        verbose_name_plural = "categorias das provas"

    def __str__(self) -> str:
        return self.name


class Event(TimeStampedModel):
    class MeasurementType(models.TextChoices):
        SECONDS = "seconds", "Segundos"
        METERS = "meters", "Metros"

    category = models.ForeignKey(
        EventCategory,
        on_delete=models.PROTECT,
        related_name="events",
        verbose_name="categoria",
    )
    measurement_type = models.CharField(
        "tipo de medição", max_length=7, choices=MeasurementType.choices
    )
    name = models.CharField("nome", max_length=255)

    class Meta:
        verbose_name = "prova"
        verbose_name_plural = "provas"

    def __str__(self) -> str:
        return self.name


class EventData(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "M", "Masculino"
        FEMALE = "F", "Feminino"

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="data", verbose_name="prova"
    )
    stage = models.ForeignKey(
        "stages.Stage",
        on_delete=models.CASCADE,
        related_name="event_data",
        verbose_name="etapa",
    )
    gender = models.CharField("naipe", max_length=1, choices=Gender.choices)
    start_time = models.TimeField("horário", null=True, blank=True)

    class Meta:
        verbose_name = "horário da prova"
        verbose_name_plural = "horários das provas"
