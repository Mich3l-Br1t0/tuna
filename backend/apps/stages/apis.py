from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Stage
from .selectors import registration_is_open, stage_get_next, stage_list


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


class StageListApi(APIView):
    """List stages with their registration window status (auth required)."""

    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        date = serializers.DateField()
        location = serializers.SerializerMethodField()
        registration_opens = serializers.DateField()
        registration_deadline = serializers.DateField()
        registration_open = serializers.SerializerMethodField()

        def get_location(self, stage: Stage) -> str | None:
            return stage.location.name if stage.location else None

        def get_registration_open(self, stage: Stage) -> bool:
            return registration_is_open(stage)

    def get(self, request: Request) -> Response:
        return Response(self.OutputSerializer(stage_list(), many=True).data)
