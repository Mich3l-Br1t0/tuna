from django.db import models

from apps.common.models import TimeStampedModel


class Location(TimeStampedModel):
    name = models.CharField("nome", max_length=255)
    address = models.CharField("endereço", max_length=255)
    lanes = models.PositiveIntegerField("raias")

    class Meta:
        verbose_name = "local"
        verbose_name_plural = "locais"

    def __str__(self) -> str:
        return self.name


class Stage(TimeStampedModel):
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name="stages",
        null=True,
        blank=True,
        verbose_name="local",
    )
    name = models.CharField("nome", max_length=255)
    date = models.DateField("data", null=True, blank=True)
    start_time = models.TimeField("horário de início", null=True, blank=True)
    end_time = models.TimeField("horário de término", null=True, blank=True)

    class Meta:
        verbose_name = "etapa"
        verbose_name_plural = "etapas"

    def __str__(self) -> str:
        return self.name


class StageMedia(TimeStampedModel):
    stage = models.ForeignKey(
        Stage, on_delete=models.CASCADE, related_name="media", verbose_name="etapa"
    )
    drive_url = models.URLField("URL do Drive")

    class Meta:
        verbose_name = "mídia da etapa"
        verbose_name_plural = "mídias da etapa"


class Rules(TimeStampedModel):
    version = models.PositiveIntegerField("versão")
    file_key = models.CharField("chave do arquivo", max_length=255)

    class Meta:
        verbose_name = "regulamento"
        verbose_name_plural = "regulamentos"

    def __str__(self) -> str:
        return f"Rules v{self.version}"
