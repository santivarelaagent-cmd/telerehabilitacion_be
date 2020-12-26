from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.authentication.models import Patient
from telerehabilitation_API.authentication.serializers import PatientSerializer


class PatientViewSet(APIView):
    def get(self, request, format=None):
        return Response(PatientSerializer(Patient.objects.all(), many=True).data)

    def post(self, request):
        if 'username' not in request.data.keys() and \
           'email' not in request.data.keys() and \
           'first_name' not in request.data.keys() and \
           'last_name' not in request.data.keys():
            return Response({}, status=400)
        else:
            new_patient = User.objects.create_user(request.data['username'], request.data['email'], '123456789')
            new_patient.first_name = request.data['first_name']
            new_patient.last_name = request.data['last_name']
            new_patient.save()
            Patient.objects.create(user_id=new_patient.id)
            return Response({}, status=201)
