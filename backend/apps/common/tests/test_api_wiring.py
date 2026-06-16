import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


def test_openapi_schema_is_served(client):
    """drf-spectacular generates the schema without errors and serves it publicly."""
    response = client.get("/api/schema/")
    assert response.status_code == 200


def test_login_endpoint_is_wired(client):
    """dj-rest-auth login route exists; bad creds return 400, not 404."""
    response = client.post("/api/auth/login/", {"username": "x", "password": "y"})
    assert response.status_code == 400


def test_password_reset_endpoint_is_wired(client):
    """Password reset accepts a request (always 200 to avoid email enumeration)."""
    response = client.post("/api/auth/password/reset/", {"email": "nobody@example.com"})
    assert response.status_code == 200
