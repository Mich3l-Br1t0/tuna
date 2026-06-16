import django_filters

from apps.universities.models import Athlete


class AthleteFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Athlete
        fields = ("name",)
