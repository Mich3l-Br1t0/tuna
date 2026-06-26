from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.athletes.models import Athlete
from apps.events.models import Event, EventCategory, EventData
from apps.registrations.models import AthleteRegister, StageRegister
from apps.stages.models import Stage
from apps.universities.models import University
from apps.users.models import User


class StageRegistrationTests(TestCase):
    """A university enrolls its athletes into a stage's provas, gated by the
    registration window and athlete eligibility."""

    def setUp(self) -> None:
        today = timezone.localdate()
        self.uni = University.objects.create(name="Uni A")
        self.other_uni = University.objects.create(name="Uni B")
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

        self.stage = Stage.objects.create(
            name="Etapa",
            date=today + timedelta(days=30),
            registration_opens=today - timedelta(days=1),
            registration_deadline=today + timedelta(days=5),
        )
        # Stage offers 100m for M and F, but 400m for F only.
        EventData.objects.create(event=self.e100, stage=self.stage, gender="M")
        EventData.objects.create(event=self.e100, stage=self.stage, gender="F")
        EventData.objects.create(event=self.e400, stage=self.stage, gender="F")

        self.male = Athlete.objects.create(name="Caio", gender="M", university=self.uni)
        self.male.events.set([self.e100, self.e400])  # capable of both
        self.female = Athlete.objects.create(
            name="Ana", gender="F", university=self.uni
        )
        self.female.events.set([self.e100, self.e400])

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def _set(self, athlete: Athlete, event_ids: list[int]):
        return self.client.post(
            f"/api/registrations/{self.stage.id}/athletes/{athlete.id}/set/",
            {"event_ids": event_ids},
            format="json",
        )

    def _rows(self, athlete: Athlete) -> list[int]:
        return list(
            AthleteRegister.objects.filter(
                stage=self.stage, athlete=athlete
            ).values_list("event_id", flat=True)
        )

    # --- registering the university ---

    def test_register_creates_stage_register(self) -> None:
        res = self.client.post(f"/api/registrations/{self.stage.id}/register/")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(
            StageRegister.objects.filter(
                university=self.uni,
                stage=self.stage,
                status=StageRegister.Status.PENDING,
            ).exists()
        )

    # --- eligibility (intersection of capability x stage offering x gender) ---

    def test_detail_eligible_events_respect_gender(self) -> None:
        data = self.client.get(f"/api/registrations/{self.stage.id}/").json()
        by_name = {a["name"]: a for a in data["athletes"]}
        male_ids = {e["id"] for e in by_name["Caio"]["eligible_events"]}
        female_ids = {e["id"] for e in by_name["Ana"]["eligible_events"]}
        # 400m is offered for women only, so the man is eligible for 100m only.
        self.assertEqual(male_ids, {self.e100.id})
        self.assertEqual(female_ids, {self.e100.id, self.e400.id})

    def test_cannot_set_ineligible_event(self) -> None:
        # 400m is not offered for men at this stage.
        res = self._set(self.male, [self.e400.id])
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self._rows(self.male), [])

    # --- the entry-set mutation: auto-enroll / deselect / remove ---

    def test_auto_enroll_all_eligible(self) -> None:
        res = self._set(self.female, [self.e100.id, self.e400.id])
        self.assertEqual(res.status_code, 200)
        self.assertCountEqual(self._rows(self.female), [self.e100.id, self.e400.id])

    def test_deselect_a_prova(self) -> None:
        self._set(self.female, [self.e100.id, self.e400.id])
        self._set(self.female, [self.e100.id])
        self.assertEqual(self._rows(self.female), [self.e100.id])

    def test_remove_athlete_with_empty_list(self) -> None:
        self._set(self.female, [self.e100.id])
        self._set(self.female, [])
        self.assertEqual(self._rows(self.female), [])

    def test_entry_set_ensures_stage_register(self) -> None:
        self._set(self.female, [self.e100.id])
        self.assertTrue(
            StageRegister.objects.filter(university=self.uni, stage=self.stage).exists()
        )

    # --- scoping ---

    def test_cannot_register_other_university_athlete(self) -> None:
        intruder = Athlete.objects.create(
            name="X", gender="F", university=self.other_uni
        )
        intruder.events.set([self.e100])
        res = self._set(intruder, [self.e100.id])
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self._rows(intruder), [])

    def test_user_without_university_rejected(self) -> None:
        admin = User.objects.create(username="admin1", role=User.Role.ADMIN)
        client = APIClient()
        client.force_authenticate(user=admin)
        res = client.post(f"/api/registrations/{self.stage.id}/register/")
        self.assertEqual(res.status_code, 400)

    # --- registration window ---

    def test_writes_rejected_after_deadline(self) -> None:
        today = timezone.localdate()
        self.stage.registration_deadline = today - timedelta(days=1)
        self.stage.save()

        res = self._set(self.female, [self.e100.id])
        self.assertEqual(res.status_code, 400)
        self.assertIn("encerrado", str(res.json()).lower())
        self.assertEqual(self._rows(self.female), [])

    def test_register_rejected_after_deadline(self) -> None:
        today = timezone.localdate()
        self.stage.registration_deadline = today - timedelta(days=1)
        self.stage.save()

        res = self.client.post(f"/api/registrations/{self.stage.id}/register/")
        self.assertEqual(res.status_code, 400)

    def test_detail_reports_registration_open(self) -> None:
        data = self.client.get(f"/api/registrations/{self.stage.id}/").json()
        self.assertTrue(data["registration_open"])

    def test_detail_lists_offered_provas_with_naipes(self) -> None:
        # 100m offered for M+F, 400m for F only.
        data = self.client.get(f"/api/registrations/{self.stage.id}/").json()
        provas = {e["name"]: e["genders"] for e in data["events"]}
        self.assertEqual([e["name"] for e in data["events"]], ["100m", "400m"])
        self.assertEqual(provas["100m"], ["M", "F"])
        self.assertEqual(provas["400m"], ["F"])
