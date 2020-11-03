from rest_framework import viewsets, permissions

from telerehabilitation_API.therapy.models import Therapy
from telerehabilitation_API.therapy.permissions import CanCreateTherapy, CanEditTherapy, CanDeleteTherapy
from telerehabilitation_API.therapy.serializers import TherapySerializer


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
