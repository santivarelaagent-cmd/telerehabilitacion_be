from rest_framework import permissions, viewsets

from telerehabilitation_API.therapy.models import Routine
from telerehabilitation_API.therapy.permissions import CanCreateRoutine, CanEditRoutine, CanDeleteRoutine
from telerehabilitation_API.therapy.serializers import RoutineSerializer


class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

    def get_permissions(self):
        permissions_classes = [permissions.IsAuthenticated]
        if self.action == 'create':
            permissions_classes.append(CanCreateRoutine)
        elif self.action in ['update', 'partial_update']:
            permissions_classes.append(CanEditRoutine)
        elif self.action == 'destroy':
            permissions_classes.append(CanDeleteRoutine)
        return [permission() for permission in permissions_classes]
