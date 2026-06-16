import pytest
from django.db import IntegrityError

from apps.universities.tests.factories import UniversityFactory
from apps.users.models import User

pytestmark = pytest.mark.django_db


def test_email_must_be_unique():
    User.objects.create_user(username="a", email="dup@example.com", password="pw")
    with pytest.raises(IntegrityError):
        User.objects.create_user(username="b", email="dup@example.com", password="pw")


def test_multiple_accounts_without_email_are_allowed():
    User.objects.create_user(username="a", password="pw")
    User.objects.create_user(username="b", password="pw")  # must not collide

    assert User.objects.filter(email__isnull=True).count() == 2


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
