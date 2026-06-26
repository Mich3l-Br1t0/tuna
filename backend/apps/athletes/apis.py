from typing import Any, cast

from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.enums import Gender
from apps.common.pagination import get_paginated_response
from apps.users.models import User

from .models import Athlete
from .selectors import athlete_list
from .services import athlete_create, athlete_delete, athlete_update


class AthleteListApi(APIView):
    """List athletes (auth required), filtered and paginated."""

    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 25
        max_limit = 50

    class FilterSerializer(serializers.Serializer):
        name = serializers.CharField(required=False, allow_blank=True)
        gender = serializers.ChoiceField(choices=Gender.choices, required=False)
        event = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        gender = serializers.CharField()
        events = serializers.SerializerMethodField()

        def get_events(self, athlete: Athlete) -> list[dict[str, Any]]:
            return [{"id": e.id, "name": e.name} for e in athlete.events.all()]

    def get(self, request: Request) -> Response:
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        filters = cast(dict[str, Any], filters_serializer.validated_data)

        user = cast(User, request.user)
        athletes = athlete_list(university=user.university, filters=filters)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=athletes,
            request=request,
            view=self,
        )


class AthleteCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        gender = serializers.ChoiceField(choices=Gender.choices)
        event_ids = serializers.ListField(
            child=serializers.IntegerField(), required=False, default=list
        )

    def post(self, request: Request) -> Response:
        user = cast(User, request.user)
        if user.university is None:
            raise ValidationError("Seu usuário não está vinculado a uma faculdade.")

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, Any], serializer.validated_data)

        athlete_create(
            name=data["name"],
            gender=data["gender"],
            university=user.university,
            event_ids=data["event_ids"],
        )

        return Response(status=status.HTTP_201_CREATED)


class AthleteUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        gender = serializers.ChoiceField(choices=Gender.choices)
        event_ids = serializers.ListField(
            child=serializers.IntegerField(), required=False, default=list
        )

    def post(self, request: Request, athlete_id: int) -> Response:
        user = cast(User, request.user)
        athlete = get_object_or_404(Athlete, id=athlete_id, university=user.university)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, Any], serializer.validated_data)

        athlete_update(
            athlete=athlete,
            name=data["name"],
            gender=data["gender"],
            event_ids=data["event_ids"],
        )

        return Response(status=status.HTTP_200_OK)


class AthleteDeleteApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, athlete_id: int) -> Response:
        user = cast(User, request.user)
        athlete = get_object_or_404(Athlete, id=athlete_id, university=user.university)

        athlete_delete(athlete=athlete)

        return Response(status=status.HTTP_204_NO_CONTENT)
