from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.athletes.models import Athlete
from apps.registrations.models import AthleteRegister
from apps.universities.models import University


class DashboardStatsView(APIView):
    """Aggregate counts for the authenticated dashboard overview."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(
            {
                "athletes": Athlete.objects.count(),
                "registrations": AthleteRegister.objects.count(),
                "universities": University.objects.count(),
            }
        )
