from django.utils import timezone

from .models import Stage


def stage_get_next() -> Stage | None:
    """The soonest stage scheduled for today or later, or None if none is set."""
    today = timezone.localdate()
    return (
        Stage.objects.filter(date__gte=today)
        .select_related("location")
        .order_by("date")
        .first()
    )
