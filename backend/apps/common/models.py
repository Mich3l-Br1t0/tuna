from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base model that adds self-updating created/modified timestamps.

    Domain models should inherit from this so audit timestamps stay consistent
    across the project instead of being redefined per model.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
