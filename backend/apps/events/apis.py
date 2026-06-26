from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import event_list


class EventListApi(APIView):
    """List all events ("provas"), auth required. Unpaginated — the set is small."""

    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        category = serializers.CharField(source="category.name")

    def get(self, request: Request) -> Response:
        events = event_list()
        return Response(self.OutputSerializer(events, many=True).data)
