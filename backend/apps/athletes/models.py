from django.db import models

from apps.common.enums import Gender
from apps.common.models import TimeStampedModel


class Athlete(TimeStampedModel):
    university = models.ForeignKey(
        "universities.University",
        on_delete=models.PROTECT,
        related_name="athletes",
        verbose_name="universidade",
    )
    name = models.CharField("nome", max_length=255)
    gender = models.CharField("sexo", max_length=1, choices=Gender.choices)
    disabled = models.BooleanField("desativado", default=False)
    events = models.ManyToManyField(
        "events.Event",
        related_name="athletes",
        blank=True,
        verbose_name="provas",
    )

    class Meta:
        verbose_name = "atleta"
        verbose_name_plural = "atletas"

    def __str__(self) -> str:
        return self.name


class RelayEntry(TimeStampedModel):
    class Team(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"

    university = models.ForeignKey(
        "universities.University",
        on_delete=models.PROTECT,
        related_name="relay_entries",
        verbose_name="universidade",
    )
    stage = models.ForeignKey(
        "stages.Stage",
        on_delete=models.CASCADE,
        related_name="relay_entries",
        verbose_name="etapa",
    )
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.PROTECT,
        related_name="relay_entries",
        verbose_name="prova",
    )
    team = models.CharField("equipe", max_length=1, choices=Team.choices)

    class Meta:
        verbose_name = "equipe de revezamento"
        verbose_name_plural = "equipes de revezamento"

    def __str__(self) -> str:
        return f"{self.university} relay {self.team}"


class RelayAthlete(TimeStampedModel):
    relay_entry = models.ForeignKey(
        RelayEntry,
        on_delete=models.CASCADE,
        related_name="athletes",
        verbose_name="equipe de revezamento",
    )
    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.PROTECT,
        related_name="relay_legs",
        verbose_name="atleta",
    )

    class Meta:
        verbose_name = "atleta do revezamento"
        verbose_name_plural = "atletas do revezamento"
