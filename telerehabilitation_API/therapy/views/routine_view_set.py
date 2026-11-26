from rest_framework import permissions, viewsets

from telerehabilitation_API.therapy.models import Routine
from telerehabilitation_API.therapy.permissions import CanCreateRoutine, CanEditRoutine, CanDeleteRoutine
from telerehabilitation_API.therapy.search_utils import filter_queryset_fuzzy
from telerehabilitation_API.therapy.serializers.routine_serializer import RoutineSerializer, RoutineListSerializer


class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all().order_by('id')
    serializer_class = RoutineSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return RoutineListSerializer
        return RoutineSerializer

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering', 'id')
        if ordering not in ('id', '-id'):
            ordering = 'id'
        if self.action == 'list':
            qs = Routine.objects.all()
            search = (self.request.query_params.get('search') or '').strip()
            if search:
                qs = filter_queryset_fuzzy(qs, search, fields=('name', 'description'))
            return qs.order_by(ordering)
        return Routine.objects.select_related('therapy').prefetch_related(
            'therapy__routines',
            'exercises__routine',
            'exercises__difficulties__ranges__point_tracked__skeleton_point',
        ).order_by(ordering)

    def get_permissions(self):
        permissions_classes = [permissions.IsAuthenticated]
        if self.action == 'create':
            permissions_classes.append(CanCreateRoutine)
        elif self.action in ['update', 'partial_update']:
            permissions_classes.append(CanEditRoutine)
        elif self.action == 'destroy':
            permissions_classes.append(CanDeleteRoutine)
        return [permission() for permission in permissions_classes]
