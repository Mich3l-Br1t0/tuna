from typing import cast

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User

from .selectors import dashboard_stats


class DashboardStatsApi(APIView):
    """Aggregate counts for the authenticated dashboard overview."""

    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        athletes = serializers.IntegerField()
        registrations = serializers.IntegerField()
        universities = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        user = cast(User, request.user)
        stats = dashboard_stats(university=user.university)

        data = self.OutputSerializer(stats).data

        return Response(data)
