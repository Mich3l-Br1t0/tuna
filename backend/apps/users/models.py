from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)

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

    def clean(self) -> None:
        super().clean()
        self._blank_email_to_none()

    def save(self, *args, **kwargs) -> None:
        self._blank_email_to_none()
        super().save(*args, **kwargs)

    def _blank_email_to_none(self) -> None:
        if not self.email:
            self.email = None
