from rest_framework import serializers

from telerehabilitation_API.therapy.models import Routine
from telerehabilitation_API.therapy.serializers.exercise_serializer import ExerciseSerializer


class RoutineSerializer(serializers.ModelSerializer):
    exercises = serializers.HyperlinkedRelatedField(many=True, view_name='exercise-detail', read_only=True)
    therapy = serializers.HyperlinkedRelatedField(view_name='therapy-detail', read_only=True)
    therapy_id = serializers.IntegerField(required=False)

    class Meta:
        model = Routine
        fields = ['id', 'therapy', 'therapy_id', 'name', 'description', 'exercises', 'is_model', 'is_active']
