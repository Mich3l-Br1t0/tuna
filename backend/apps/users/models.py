from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Project user model.

    User type is relationship-driven, not an enum:
    - ``university`` set  -> a university account (manages that university's athletes).
    - ``university`` null + ``is_staff`` -> an admin (manages the system via the admin).
    """

    email = models.EmailField(unique=True)

    university = models.OneToOneField(
        "universities.University",
        on_delete=models.CASCADE,
        related_name="account",
        null=True,
        blank=True,
    )

    REQUIRED_FIELDS = ["email"]

    @property
    def is_university_account(self) -> bool:
        return self.university_id is not None
