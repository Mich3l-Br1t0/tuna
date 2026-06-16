import pytest
from django.db import IntegrityError

from apps.universities.models import Athlete, University
from apps.universities.tests.factories import AthleteFactory, UniversityFactory

pytestmark = pytest.mark.django_db


def test_university_name_is_unique():
    UniversityFactory(name="Tuna Tech")
    with pytest.raises(IntegrityError):
        UniversityFactory(name="Tuna Tech")


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
