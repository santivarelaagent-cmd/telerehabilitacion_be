from rest_framework import serializers

from telerehabilitation_API.therapy.models import TherapyPatient


class TherapyPatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = TherapyPatient
        fields = '__all__'
