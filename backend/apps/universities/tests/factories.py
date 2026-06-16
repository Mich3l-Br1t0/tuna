# factory_boy ships no type stubs, so pyright misreads its public API as private.
# pyright: reportPrivateImportUsage=false
import factory

from apps.universities.models import Athlete, University


class UniversityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = University

    name = factory.Sequence(lambda n: f"University {n}")


class AthleteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Athlete

    university = factory.SubFactory(UniversityFactory)
    name = factory.Sequence(lambda n: f"Athlete {n}")
