from django.db import models

from apps.common.models import TimeStampedModel


class StageRegister(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pendente"
        SUBMITTED = "Submitted", "Enviada"
        CONFIRMED = "Confirmed", "Confirmada"

    university = models.ForeignKey(
        "universities.University",
        on_delete=models.PROTECT,
        related_name="stage_registrations",
        verbose_name="universidade",
    )
    stage = models.ForeignKey(
        "stages.Stage",
        on_delete=models.CASCADE,
        related_name="registrations",
        verbose_name="etapa",
    )
    status = models.CharField(
        "situação", max_length=9, choices=Status.choices, default=Status.PENDING
    )
    payment_proof_key = models.CharField(
        "comprovante de pagamento", max_length=255, blank=True, default=""
    )

    class Meta:
        verbose_name = "inscrição de etapa"
        verbose_name_plural = "inscrições de etapa"
        constraints = [
            models.UniqueConstraint(
                fields=["university", "stage"], name="unique_university_per_stage"
            )
        ]


class AthleteRegister(TimeStampedModel):
    stage = models.ForeignKey(
        "stages.Stage",
        on_delete=models.CASCADE,
        related_name="athlete_registrations",
        verbose_name="etapa",
    )
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.PROTECT,
        related_name="athlete_registrations",
        verbose_name="prova",
    )
    athlete = models.ForeignKey(
        "athletes.Athlete",
        on_delete=models.PROTECT,
        related_name="registrations",
        verbose_name="atleta",
    )

    class Meta:
        verbose_name = "inscrição de atleta"
        verbose_name_plural = "inscrições de atleta"
        constraints = [
            models.UniqueConstraint(
                fields=["stage", "event", "athlete"],
                name="unique_athlete_event_per_stage",
            )
        ]
