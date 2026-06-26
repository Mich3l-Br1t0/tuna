from django.db.models import QuerySet
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


def stage_list() -> QuerySet[Stage]:
    return Stage.objects.select_related("location").order_by("-date")


def registration_is_open(stage: Stage) -> bool:
    """Registration is open from the start of `registration_opens` (or always,
    if unset) through the end of `registration_deadline`."""
    if stage.registration_deadline is None:
        return False
    today = timezone.localdate()
    if stage.registration_opens is not None and today < stage.registration_opens:
        return False
    return today <= stage.registration_deadline
