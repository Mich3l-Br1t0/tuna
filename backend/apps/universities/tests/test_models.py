import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.universities.models import Athlete, University
from apps.universities.tests.factories import AthleteFactory, UniversityFactory

pytestmark = pytest.mark.django_db


def test_normalized_name_transliterates_accents_and_case():
    university = University.objects.create(name="Universidade de São Paulo")
    assert university.normalized_name == "universidade de sao paulo"


def test_accent_or_case_variant_collides_at_db_level():
    University.objects.create(name="Universidade de São Paulo")
    with pytest.raises(IntegrityError):
        University.objects.create(name="universidade de sao paulo")


def test_duplicate_surfaces_friendly_error_on_full_clean():
    University.objects.create(name="Universidade de São Paulo")
    duplicate = University(name="UNIVERSIDADE DE SAO PAULO")
    with pytest.raises(ValidationError) as exc:
        duplicate.full_clean()
    assert "name" in exc.value.message_dict


def test_athlete_belongs_to_university_via_related_name():
    university = UniversityFactory()
    athlete = AthleteFactory(university=university)
    assert athlete in university.athletes.all()


def test_deleting_university_cascades_to_athletes():
    university = UniversityFactory()
    AthleteFactory.create_batch(3, university=university)
    assert Athlete.objects.count() == 3

    university.delete()
    assert Athlete.objects.count() == 0
    assert University.objects.count() == 0
