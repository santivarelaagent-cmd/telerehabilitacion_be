from rest_framework import serializers

from telerehabilitation_API.therapy.models import ExerciseSkeletonPointTracked
from telerehabilitation_API.therapy.serializers import SkeletonPointSerializer


class ExerciseSkeletonPointTrackedSerializer(serializers.ModelSerializer):
    skeleton_point = SkeletonPointSerializer(required=False)

    class Meta:
        model = ExerciseSkeletonPointTracked
        fields = ['skeleton_point', 'skeleton_point_id', 'exercise_id', 'max_angle', 'min_angle']