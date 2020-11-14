from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from telerehabilitation_API.therapy.models import Exercise, ExerciseSkeletonPointTracked
from telerehabilitation_API.therapy.permissions import CanCreateExercise, CanEditExercise, CanDeleteExercise
from telerehabilitation_API.therapy.serializers import ExerciseSerializer
from telerehabilitation_API.therapy.serializers.exercise_video_serializer import ExerciseVideoSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def create(self, request, *args, **kwargs):
        exercise_serialized = self.get_serializer(data=request.data)
        exercise_serialized.is_valid(raise_exception=True)
        self.perform_create(exercise_serialized)
        headers = self.get_success_headers(exercise_serialized.data)
        return Response(exercise_serialized.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        permissions_classes = [permissions.IsAuthenticated]
        if self.action == 'create':
            permissions_classes.append(CanCreateExercise)
        elif self.action in ['update', 'partial_update']:
            permissions_classes.append(CanEditExercise)
        elif self.action == 'destroy':
            permissions_classes.append(CanDeleteExercise)
        return [permission() for permission in permissions_classes]

    @action(methods=['post'], detail=True)
    def video(self, request, pk=None):
        exercise = self.get_object()
        video_serialized = ExerciseVideoSerializer(data=request.data)
        errors = []
        if not video_serialized.is_valid():
            errors.append({ 'video': video_serialized.error_messages})
        if 'points' not in request.data:
            errors.append({ 'points': 'There is no points' })
        if not errors:
            for point in request.data['points'].split(','):
                point_tracked = ExerciseSkeletonPointTracked(exercise=exercise, skeleton_point_id=int(point))
                point_tracked.save()
            exercise.video = request.data['video']
            exercise.save()
            return Response(status=200)
        return Response({'errors': errors}, status=400)
