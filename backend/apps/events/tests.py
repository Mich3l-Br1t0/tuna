from django.test import TestCase
from rest_framework.test import APIClient

from apps.events.models import Event, EventCategory
from apps.users.models import User


class EventListApiTests(TestCase):
    def setUp(self) -> None:
        cat = EventCategory.objects.create(
            name="Corrida", type=EventCategory.Type.TRACK
        )
        Event.objects.create(
            category=cat, measurement_type=Event.MeasurementType.SECONDS, name="100m"
        )
        self.client = APIClient()

    def test_requires_authentication(self) -> None:
        self.assertIn(self.client.get("/api/events/").status_code, (401, 403))

    def test_lists_events(self) -> None:
        self.client.force_authenticate(user=User.objects.create(username="u"))
        data = self.client.get("/api/events/").json()
        self.assertEqual([e["name"] for e in data], ["100m"])
        self.assertEqual(data[0]["category"], "Corrida")
