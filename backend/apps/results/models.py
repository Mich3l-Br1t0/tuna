from django.db import models

from apps.common.models import TimeStampedModel


class Result(TimeStampedModel):
    class Status(models.TextChoices):
        COMPLETED = "Completed", "Concluído"
        DNF = "DNF", "Não Terminou"
        DNS = "DNS", "Não Largou"
        DQ = "DQ", "Desclassificado"

    # Exactly one of these is set (enforced by the check constraint below).
    athlete_register = models.ForeignKey(
        "registrations.AthleteRegister",
        on_delete=models.CASCADE,
        related_name="results",
        null=True,
        blank=True,
        verbose_name="inscrição do atleta",
    )
    relay_entry = models.ForeignKey(
        "athletes.RelayEntry",
        on_delete=models.CASCADE,
        related_name="results",
        null=True,
        blank=True,
        verbose_name="equipe de revezamento",
    )
    status = models.CharField("situação", max_length=9, choices=Status.choices)
    position = models.PositiveIntegerField("posição")
    result = models.DecimalField(
        "resultado", max_digits=10, decimal_places=3, null=True, blank=True
    )
    is_record = models.BooleanField("é recorde", default=False)

    class Meta:
        verbose_name = "resultado"
        verbose_name_plural = "resultados"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(athlete_register__isnull=False, relay_entry__isnull=True)
                    | models.Q(athlete_register__isnull=True, relay_entry__isnull=False)
                ),
                name="result_exactly_one_entry",
            )
        ]
