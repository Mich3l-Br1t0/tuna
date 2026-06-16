import pytest
from rest_framework.test import APIClient

from apps.universities.models import Athlete
from apps.universities.tests.factories import AthleteFactory, UniversityFactory
from apps.users.models import User

pytestmark = pytest.mark.django_db

LIST_URL = "/api/athletes/"


def detail_url(athlete_id: int) -> str:
    return f"/api/athletes/{athlete_id}/"


@pytest.fixture
def university():
    return UniversityFactory()


@pytest.fixture
def account(university):
    return User.objects.create_user(
        username="uni-acc", email="uni@example.com", password="pw", university=university
    )


@pytest.fixture
def client(account):
    api_client = APIClient()
    api_client.force_authenticate(user=account)
    return api_client


def test_list_returns_only_own_universitys_athletes(client, university):
    AthleteFactory.create_batch(2, university=university)
    AthleteFactory.create_batch(3, university=UniversityFactory())  # another university

    response = client.get(LIST_URL)

    assert response.status_code == 200
    assert response.data["count"] == 2


def test_filter_by_name(client, university):
    AthleteFactory(university=university, name="Alice")
    AthleteFactory(university=university, name="Bob")

    response = client.get(LIST_URL, {"name": "ali"})

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "Alice"


def test_create_athlete_under_own_university(client, university):
    response = client.post(LIST_URL, {"name": "Jane Doe"}, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Jane Doe"
    athlete = Athlete.objects.get(id=response.data["id"])
    assert athlete.university == university


def test_retrieve_athlete(client, university):
    athlete = AthleteFactory(university=university)

    response = client.get(detail_url(athlete.id))

    assert response.status_code == 200
    assert response.data["id"] == athlete.id


def test_update_athlete(client, university):
    athlete = AthleteFactory(university=university, name="Old")

    response = client.patch(detail_url(athlete.id), {"name": "New"}, format="json")

    assert response.status_code == 200
    athlete.refresh_from_db()
    assert athlete.name == "New"


def test_delete_athlete(client, university):
    athlete = AthleteFactory(university=university)

    response = client.delete(detail_url(athlete.id))

    assert response.status_code == 204
    assert not Athlete.objects.filter(id=athlete.id).exists()


def test_cannot_touch_another_universitys_athlete(client):
    foreign = AthleteFactory(university=UniversityFactory())

    assert client.get(detail_url(foreign.id)).status_code == 404
    assert client.patch(detail_url(foreign.id), {"name": "x"}, format="json").status_code == 404
    assert client.delete(detail_url(foreign.id)).status_code == 404
    assert Athlete.objects.filter(id=foreign.id).exists()  # untouched


def test_admin_without_university_is_forbidden(university):
    admin = User.objects.create_user(
        username="admin", email="admin@example.com", password="pw", is_staff=True
    )
    api_client = APIClient()
    api_client.force_authenticate(user=admin)

    assert api_client.get(LIST_URL).status_code == 403


def test_unauthenticated_is_rejected():
    response = APIClient().get(LIST_URL)
    assert response.status_code in (401, 403)
