from rest_framework import serializers


class ExerciseResultsVideoSerializer(serializers.Serializer):
    video = serializers.URLField(required=True)
