from django.test import TestCase
from rest_framework.test import APIClient

from apps.athletes.models import Athlete
from apps.events.models import Event, EventCategory
from apps.universities.models import University
from apps.users.models import User


class AthleteScopingTests(TestCase):
    """Athletes are scoped to the caller's faculty for read AND write."""

    def setUp(self) -> None:
        self.uni_a = University.objects.create(name="Uni A")
        self.uni_b = University.objects.create(name="Uni B")
        self.user_a = User.objects.create(
            username="rep_a", role=User.Role.USER, university=self.uni_a
        )
        self.athlete_a = Athlete.objects.create(
            name="Ana", gender="F", university=self.uni_a
        )
        self.athlete_b = Athlete.objects.create(
            name="Bruno", gender="M", university=self.uni_b
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_a)

    def test_list_is_scoped_to_user_university(self) -> None:
        names = [a["name"] for a in self.client.get("/api/athletes/").json()["results"]]
        self.assertEqual(names, ["Ana"])

    def test_cannot_delete_other_university_athlete(self) -> None:
        res = self.client.post(f"/api/athletes/{self.athlete_b.id}/delete/")
        self.assertEqual(res.status_code, 404)
        self.assertTrue(Athlete.objects.filter(id=self.athlete_b.id).exists())

    def test_cannot_update_other_university_athlete(self) -> None:
        res = self.client.post(
            f"/api/athletes/{self.athlete_b.id}/update/",
            {"name": "hacked", "gender": "M"},
            format="json",
        )
        self.assertEqual(res.status_code, 404)

    def test_can_delete_own_athlete(self) -> None:
        res = self.client.post(f"/api/athletes/{self.athlete_a.id}/delete/")
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Athlete.objects.filter(id=self.athlete_a.id).exists())


class AthleteEventsTests(TestCase):
    """Athletes carry the provas they can compete in, set on create/update."""

    def setUp(self) -> None:
        self.uni = University.objects.create(name="Uni")
        self.user = User.objects.create(
            username="rep", role=User.Role.USER, university=self.uni
        )
        cat = EventCategory.objects.create(
            name="Corrida", type=EventCategory.Type.TRACK
        )
        self.e100 = Event.objects.create(
            category=cat, measurement_type=Event.MeasurementType.SECONDS, name="100m"
        )
        self.e400 = Event.objects.create(
            category=cat, measurement_type=Event.MeasurementType.SECONDS, name="400m"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_with_events_assigns_them(self) -> None:
        res = self.client.post(
            "/api/athletes/create/",
            {
                "name": "Carlos",
                "gender": "M",
                "event_ids": [self.e100.id, self.e400.id],
            },
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        athlete = Athlete.objects.get(name="Carlos")
        self.assertCountEqual(
            athlete.events.values_list("id", flat=True),
            [self.e100.id, self.e400.id],
        )

    def test_list_output_includes_events(self) -> None:
        athlete = Athlete.objects.create(name="Dora", gender="F", university=self.uni)
        athlete.events.set([self.e100])
        row = next(
            a
            for a in self.client.get("/api/athletes/").json()["results"]
            if a["name"] == "Dora"
        )
        self.assertEqual(row["events"], [{"id": self.e100.id, "name": "100m"}])

    def test_update_replaces_events(self) -> None:
        athlete = Athlete.objects.create(name="Edu", gender="M", university=self.uni)
        athlete.events.set([self.e100])
        res = self.client.post(
            f"/api/athletes/{athlete.id}/update/",
            {"name": "Edu", "gender": "M", "event_ids": [self.e400.id]},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(athlete.events.values_list("id", flat=True)), [self.e400.id]
        )

    def test_filter_by_event(self) -> None:
        sprinter = Athlete.objects.create(
            name="Sprint", gender="M", university=self.uni
        )
        sprinter.events.set([self.e100])
        miler = Athlete.objects.create(name="Mile", gender="M", university=self.uni)
        miler.events.set([self.e400])

        results = self.client.get(f"/api/athletes/?event={self.e100.id}").json()[
            "results"
        ]
        self.assertEqual([a["name"] for a in results], ["Sprint"])
