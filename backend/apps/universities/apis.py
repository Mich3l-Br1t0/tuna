from typing import cast

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.pagination import LimitOffsetPagination, get_paginated_response
from apps.common.permissions import IsUniversityAccount
from apps.universities import selectors, services
from apps.universities.models import University
from apps.universities.serializers import (
    AthleteFilterSerializer,
    AthleteInputSerializer,
    AthleteOutputSerializer,
)
from apps.users.models import User


def _request_university(request: Request) -> University:
    return cast(University, cast(User, request.user).university)


class AthleteListCreateApi(APIView):
    permission_classes = (IsUniversityAccount,)

    @extend_schema(
        operation_id="athletes_list",
        parameters=[AthleteFilterSerializer],
        responses=AthleteOutputSerializer(many=True),
    )
    def get(self, request: Request) -> Response:
        filter_serializer = AthleteFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        athletes = selectors.athlete_list(
            university=_request_university(request),
            filters=filter_serializer.validated_data,
        )
        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=AthleteOutputSerializer,
            queryset=athletes,
            request=request,
            view=self,
        )

    @extend_schema(
        operation_id="athletes_create",
        request=AthleteInputSerializer,
        responses=AthleteOutputSerializer,
    )
    def post(self, request: Request) -> Response:
        serializer = AthleteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        athlete = services.athlete_create(
            university=_request_university(request),
            **serializer.validated_data,
        )
        return Response(AthleteOutputSerializer(athlete).data, status=status.HTTP_201_CREATED)


class AthleteDetailApi(APIView):
    permission_classes = (IsUniversityAccount,)

    @extend_schema(operation_id="athletes_retrieve", responses=AthleteOutputSerializer)
    def get(self, request: Request, athlete_id: int) -> Response:
        athlete = selectors.athlete_get(
            university=_request_university(request), athlete_id=athlete_id
        )
        return Response(AthleteOutputSerializer(athlete).data)

    @extend_schema(
        operation_id="athletes_update",
        request=AthleteInputSerializer,
        responses=AthleteOutputSerializer,
    )
    def patch(self, request: Request, athlete_id: int) -> Response:
        athlete = selectors.athlete_get(
            university=_request_university(request), athlete_id=athlete_id
        )
        serializer = AthleteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        athlete = services.athlete_update(athlete=athlete, **serializer.validated_data)
        return Response(AthleteOutputSerializer(athlete).data)

    @extend_schema(operation_id="athletes_delete", responses={204: None})
    def delete(self, request: Request, athlete_id: int) -> Response:
        athlete = selectors.athlete_get(
            university=_request_university(request), athlete_id=athlete_id
        )
        services.athlete_delete(athlete=athlete)
        return Response(status=status.HTTP_204_NO_CONTENT)
