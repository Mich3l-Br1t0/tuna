from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import site_content_get


class SiteContentDetailApi(APIView):
    """Public, read-only home-page content (the single SiteContent row)."""

    permission_classes = [AllowAny]

    class OutputSerializer(serializers.Serializer):
        historico = serializers.CharField()
        o_torneio = serializers.CharField()
        proxima_etapa = serializers.CharField()
        regulamento_url = serializers.URLField()
        contato_email = serializers.EmailField()
        instagram_url = serializers.URLField()
        facebook_url = serializers.URLField()

    def get(self, request: Request) -> Response:
        content = site_content_get()

        data = self.OutputSerializer(content).data

        return Response(data)
