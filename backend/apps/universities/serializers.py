from rest_framework import serializers


class AthleteOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class AthleteInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class AthleteFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
