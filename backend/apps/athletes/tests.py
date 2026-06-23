from django.test import TestCase
from rest_framework.test import APIClient

from apps.athletes.models import Athlete
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
