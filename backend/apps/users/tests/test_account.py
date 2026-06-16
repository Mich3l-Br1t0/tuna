import pytest
from django.core import mail
from django.db import IntegrityError

from apps.universities.tests.factories import UniversityFactory
from apps.users import services
from apps.users.models import User

pytestmark = pytest.mark.django_db


def test_email_must_be_unique():
    User.objects.create_user(username="a", email="dup@example.com", password="pw")
    with pytest.raises(IntegrityError):
        User.objects.create_user(username="b", email="dup@example.com", password="pw")


def test_university_link_is_one_to_one():
    university = UniversityFactory()
    User.objects.create_user(
        username="acc1", email="acc1@example.com", password="pw", university=university
    )
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username="acc2", email="acc2@example.com", password="pw", university=university
        )


def test_is_university_account_and_reverse_relation():
    university = UniversityFactory()
    admin = User.objects.create_user(username="admin", email="admin@example.com", password="pw")
    account = User.objects.create_user(
        username="uni", email="uni@example.com", password="pw", university=university
    )

    assert admin.is_university_account is False
    assert account.is_university_account is True
    assert university.account == account  # reverse OneToOne accessor


def test_create_university_account_sends_invite_without_usable_password():
    university = UniversityFactory()

    user = services.create_university_account(
        username="newuni", email="new@example.com", university=university
    )

    assert user.is_university_account is True
    assert user.has_usable_password() is False  # password set only via the emailed link
    assert len(mail.outbox) == 1
    assert "new@example.com" in mail.outbox[0].to
