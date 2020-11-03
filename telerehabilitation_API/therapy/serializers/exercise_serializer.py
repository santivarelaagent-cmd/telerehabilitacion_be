from rest_framework import serializers

from telerehabilitation_API.therapy.models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    routine = serializers.HyperlinkedRelatedField(view_name='routine-detail', read_only=True)
    routine_id = serializers.IntegerField(required=False)

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'order', 'routine', 'routine_id', 'is_model', 'is_active']
