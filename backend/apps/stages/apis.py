from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Stage
from .selectors import stage_get_next


class StageNextApi(APIView):
    """Public: the next upcoming stage (etapa), or null if none is scheduled."""

    permission_classes = [AllowAny]

    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        date = serializers.DateField()
        location = serializers.SerializerMethodField()

        def get_location(self, stage: Stage) -> str | None:
            return stage.location.name if stage.location else None

    def get(self, request: Request) -> Response:
        stage = stage_get_next()
        data = self.OutputSerializer(stage).data if stage else None
        return Response(data)
