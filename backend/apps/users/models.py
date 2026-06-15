from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Project user model.

    Kept intentionally thin for the skeleton phase: it currently mirrors Django's
    default user. It exists now only so ``AUTH_USER_MODEL`` points at our own model
    from the first migration — swapping the user model later is highly disruptive.
    Domain fields (e.g. a link to a university) are added in the data-modeling phase.
    """
