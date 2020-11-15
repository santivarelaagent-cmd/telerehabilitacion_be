from rest_framework import serializers

from telerehabilitation_API.therapy.models import Exercise

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)

class ExerciseSerializer(serializers.ModelSerializer):
    routine = serializers.HyperlinkedRelatedField(view_name='routine-detail', read_only=True)
    routine_id = serializers.IntegerField(required=False)
    status = ChoiceField(choices=Exercise.EXERCISE_STATUS)

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'order', 'routine', 'routine_id', 'status', 'is_model', 'is_active']
