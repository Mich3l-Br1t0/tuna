from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.stages.models import Stage
from apps.users.models import User


class StageListApiTests(TestCase):
    """The stage list tells the frontend whether registration is currently open."""

    def setUp(self) -> None:
        today = timezone.localdate()
        self.open_stage = Stage.objects.create(
            name="Aberta",
            date=today + timedelta(days=30),
            registration_opens=today - timedelta(days=1),
            registration_deadline=today + timedelta(days=5),
        )
        self.closed_stage = Stage.objects.create(
            name="Encerrada",
            date=today + timedelta(days=30),
            registration_opens=today - timedelta(days=10),
            registration_deadline=today - timedelta(days=1),
        )
        self.client = APIClient()
        self.client.force_authenticate(user=User.objects.create(username="u"))

    def test_registration_open_flag(self) -> None:
        by_name = {s["name"]: s for s in self.client.get("/api/stages/").json()}
        self.assertTrue(by_name["Aberta"]["registration_open"])
        self.assertFalse(by_name["Encerrada"]["registration_open"])
