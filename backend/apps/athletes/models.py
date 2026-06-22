from django.db import models

from apps.common.models import TimeStampedModel


class Athlete(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    university = models.ForeignKey(
        "universities.University", on_delete=models.PROTECT, related_name="athletes"
    )
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=Gender.choices)

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
    )
    stage = models.ForeignKey(
        "stages.Stage", on_delete=models.CASCADE, related_name="relay_entries"
    )
    event = models.ForeignKey(
        "events.Event", on_delete=models.PROTECT, related_name="relay_entries"
    )
    team = models.CharField(max_length=1, choices=Team.choices)

    def __str__(self) -> str:
        return f"{self.university} relay {self.team}"


class RelayAthlete(TimeStampedModel):
    relay_entry = models.ForeignKey(
        RelayEntry, on_delete=models.CASCADE, related_name="athletes"
    )
    athlete = models.ForeignKey(
        Athlete, on_delete=models.PROTECT, related_name="relay_legs"
    )
