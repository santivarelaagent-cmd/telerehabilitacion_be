from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.authentication.models import Patient
from telerehabilitation_API.authentication.serializers import PatientSerializer


class PatientViewSet(APIView):
    def get(self, request, format=None):
        return Response(PatientSerializer(Patient.objects.all(), many=True).data)
