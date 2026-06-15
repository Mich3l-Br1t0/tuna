import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


def test_custom_user_model_is_used():
    """The active user model should be our own users.User, not Django's default."""
    User = get_user_model()
    assert User._meta.app_label == "users"
    assert User.__name__ == "User"


def test_create_user():
    User = get_user_model()
    user = User.objects.create_user(username="uni", password="secret-pass-123")
    assert user.pk is not None
    assert user.check_password("secret-pass-123")
