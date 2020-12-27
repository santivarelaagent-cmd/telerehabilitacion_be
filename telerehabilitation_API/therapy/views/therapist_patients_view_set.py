from lib2to3.fixes.fix_input import context

from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.authentication.serializers import UserModelSerializer
from telerehabilitation_API.therapy.models import TherapyPatient
from telerehabilitation_API.therapy.serializers import TherapyPatientSerializer


class TherapistPatientsViewSet(APIView):
    def get(self, request):
        therapist_id = request.GET.get('therapist_id', 'NOT_FOUND')
        patient_id = request.GET.get('patient_id', 'NOT_FOUND')
        if therapist_id == 'NOT_FOUND':
            if patient_id == 'NOT_FOUND':
                return Response([], status=400)
            try:
                patients_json = TherapyPatientSerializer(
                    TherapyPatient.objects.filter(id=int(patient_id)),
                    many=True,
                    context={'request': request}
                ).data

                return Response(patients_json[0], status=200)
            except TherapyPatient.DoesNotExist:
                return Response([], status=404)
        else:
            try:
                patients_json = TherapyPatientSerializer(
                    TherapyPatient.objects.filter(therapist__user_id=int(therapist_id)).all(),
                    many=True,
                    context={'request': request}
                ).data

                return Response(patients_json, status=200)
            except TherapyPatient.DoesNotExist:
                return Response([], status=404)
