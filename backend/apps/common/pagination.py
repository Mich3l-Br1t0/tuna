from typing import Any

from django.db.models import QuerySet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView


def get_paginated_response(
    *,
    pagination_class: type[LimitOffsetPagination],
    serializer_class: type[BaseSerializer],
    queryset: QuerySet[Any],
    request: Request,
    view: APIView,
) -> Response:
    """HackSoft-style helper: paginate `queryset`, serialize the page, and wrap it
    in the paginator's `{count, next, previous, results}` envelope."""
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)
    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return Response(data=serializer.data)
