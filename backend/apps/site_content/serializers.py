from rest_framework import serializers

from .models import SiteContent


class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = [
            "historico",
            "o_torneio",
            "proxima_etapa",
            "regulamento_url",
            "contato_email",
            "instagram_url",
            "facebook_url",
        ]
