from typing import Any, cast

from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.athletes.models import Athlete
from apps.stages.models import Stage
from apps.stages.selectors import registration_is_open
from apps.universities.models import University
from apps.users.models import User

from .selectors import (
    registration_athletes,
    stage_offered_provas,
    stage_register_get,
)
from .services import athlete_entry_set, stage_register_create


def _university_or_403(request: Request) -> University:
    user = cast(User, request.user)
    if user.university is None:
        raise ValidationError("Seu usuário não está vinculado a uma faculdade.")
    return user.university


class StageRegisterDetailApi(APIView):
    """The university's registration for a stage: status + manageable athletes."""

    permission_classes = [IsAuthenticated]

    class EventSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()

    class AthleteSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        gender = serializers.CharField()
        eligible_events = serializers.ListField()
        selected_event_ids = serializers.ListField(child=serializers.IntegerField())

    def get(self, request: Request, stage_id: int) -> Response:
        university = _university_or_403(request)
        stage = get_object_or_404(Stage, id=stage_id)
        register = stage_register_get(university=university, stage=stage)

        return Response(
            {
                "status": register.status if register else None,
                "registration_open": registration_is_open(stage),
                "events": stage_offered_provas(stage=stage),
                "athletes": self.AthleteSerializer(
                    registration_athletes(university=university, stage=stage),
                    many=True,
                ).data,
            }
        )


class StageRegisterCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, stage_id: int) -> Response:
        university = _university_or_403(request)
        stage = get_object_or_404(Stage, id=stage_id)
        stage_register_create(university=university, stage=stage)
        return Response(status=status.HTTP_201_CREATED)


class AthleteEntrySetApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        event_ids = serializers.ListField(
            child=serializers.IntegerField(), allow_empty=True
        )

    def post(self, request: Request, stage_id: int, athlete_id: int) -> Response:
        university = _university_or_403(request)
        stage = get_object_or_404(Stage, id=stage_id)
        athlete = get_object_or_404(Athlete, id=athlete_id)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, Any], serializer.validated_data)

        athlete_entry_set(
            university=university,
            stage=stage,
            athlete=athlete,
            event_ids=data["event_ids"],
        )
        return Response(status=status.HTTP_200_OK)
