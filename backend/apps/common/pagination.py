from typing import Any

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


def get_paginated_response(
    *,
    pagination_class: type[_LimitOffsetPagination],
    serializer_class: type[Serializer],
    queryset: Any,
    request: Request,
    view: APIView,
) -> Response:
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)
    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return Response(data=serializer.data)
