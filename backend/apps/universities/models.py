import unicodedata

from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import TimeStampedModel


class University(TimeStampedModel):
    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255, unique=True, editable=False)

    class Meta:
        verbose_name_plural = "universities"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def _normalize_name(value: str) -> str:
        decomposed = unicodedata.normalize("NFKD", value)
        ascii_value = decomposed.encode("ascii", "ignore").decode("ascii")
        return " ".join(ascii_value.lower().split())

    def clean(self) -> None:
        super().clean()
        self.normalized_name = self._normalize_name(self.name)
        if self.normalized_name:
            duplicates = University.objects.filter(normalized_name=self.normalized_name)
            if self.pk:
                duplicates = duplicates.exclude(pk=self.pk)
            if duplicates.exists():
                raise ValidationError({"name": "A university with a similar name already exists."})

    def save(self, *args, **kwargs) -> None:
        # Keep the key correct even on saves that bypass full_clean().
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)


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
