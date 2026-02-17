from rest_framework import serializers


class ExerciseVideoSerializer(serializers.Serializer):
    video = serializers.URLField(required=True)
