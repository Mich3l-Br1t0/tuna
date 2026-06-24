from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Role.ADMIN)
        extra_fields["university"] = None
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        USER = "USER", "Usuário"

    role = models.CharField(
        "função", max_length=5, choices=Role.choices, default=Role.USER
    )
    # null university => admin account
    university = models.OneToOneField(
        "universities.University",
        on_delete=models.CASCADE,
        related_name="account",
        null=True,
        blank=True,
        verbose_name="universidade",
    )

    objects = UserManager()

    @property
    def is_university_account(self) -> bool:
        # university_id is Django-synthesized (not seen by the type checker)
        return self.university_id is not None  # pyright: ignore[reportAttributeAccessIssue]
