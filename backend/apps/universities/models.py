from django.db import models

from apps.common.models import TimeStampedModel


class University(TimeStampedModel):
    name = models.CharField("nome", max_length=255, unique=True)

    class Meta:
        verbose_name = "universidade"
        verbose_name_plural = "universidades"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
