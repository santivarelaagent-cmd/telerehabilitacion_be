import json

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from telerehabilitation_API.therapy.models import Therapy, TherapyPatient
from telerehabilitation_API.therapy.permissions import CanCreateTherapy, CanEditTherapy, CanDeleteTherapy
from telerehabilitation_API.therapy.serializers import TherapySerializer, RoutineSerializer
from telerehabilitation_API.authentication.serializers import PatientSerializer


class TherapyViewSet(viewsets.ModelViewSet):
    queryset = Therapy.objects.all()
    serializer_class = TherapySerializer

    def get_permissions(self):
        permissions_classes = [permissions.IsAuthenticated]
        if self.action == 'create':
            permissions_classes.append(CanCreateTherapy)
        elif self.action in ['update', 'partial_update']:
            permissions_classes.append(CanEditTherapy)
        elif self.action == 'destroy':
            permissions_classes.append(CanDeleteTherapy)
        return [permission() for permission in permissions_classes]

    @action(methods=['get'], detail=True)
    def get_patients(self, request, pk=None):
        return Response(
            [{
                'id': x.id,
                'patient': PatientSerializer(x.patient).data
            } for x in self.get_object().patients.all()
            ]
        )

    @action(methods=['post'], detail=True)
    def enroll_patient(self, request, pk=None):
        therapy = self.get_object()
        body = request.data
        TherapyPatient.objects.create(
            therapist_id=body['therapist'],
            therapy_id=body['therapy'],
            patient_id=body['patient']
        )
        return Response(body)

    @action(methods=['get'], detail=True)
    def routines(self, request, pk=None):
        therapy = self.get_object()
        return Response(RoutineSerializer(therapy.routines.all(), many=True, context={'request': request}).data)
