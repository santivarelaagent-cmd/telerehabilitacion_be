import json

from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from telerehabilitation_API.therapy.models import Exercise, ExerciseSkeletonPointTracked, ExerciseDifficulty, \
    DifficultyRange
from telerehabilitation_API.therapy.permissions import CanCreateExercise, CanEditExercise, CanDeleteExercise
from telerehabilitation_API.therapy.serializers import ExerciseSerializer, SkeletonPointSerializer
from telerehabilitation_API.therapy.serializers.exercise_difficulty_serializer import ExerciseDifficultySerializer
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
            ExerciseSkeletonPointTracked.objects.filter(exercise=exercise).delete()
            for point in request.data['points'].split(','):
                point_tracked = ExerciseSkeletonPointTracked(exercise=exercise, skeleton_point_id=int(point))
                point_tracked.save()
            
            try:
                exercise.video = request.data['video']
                exercise.status = Exercise.PROCESSING
                exercise.save()
            except Exception as e:
                exercise.status = Exercise.ERROR
                exercise.save()
            return Response({}, status=200)
        return Response({'errors': errors}, status=400)

    @action(methods=['post'], detail=True)
    def video_results(self, request, pk=None):
        exercise = self.get_object()
        errors = []
        if 'error' not in request.data or 'results' not in request.data:
            return Response(status=400)
        if request.data['error']:
            exercise.status = Exercise.ERROR
            exercise.save()
        else:
            exercise.status = Exercise.PROCESSED
            exercise.save()
            recieved_data = request.data['results']
            points = recieved_data['points']
            for point_tracked in ExerciseSkeletonPointTracked.objects.filter(exercise=exercise).all():
                point = next(x for x in points if x['center'] == point_tracked.skeleton_point.codename)
                point_tracked.max_angle = float(point['max_angle'])
                point_tracked.min_angle= float(point['min_angle'])
                point_tracked.save()
        return Response(status=200)

    @action(methods=['get'], detail=True)
    def points_tracked(self, request, pk=None):
        exercise = self.get_object()
        points = []
        for point in exercise.tracked_points.all():
            point_serialized = SkeletonPointSerializer(point.skeleton_point).data
            point_serialized.update({'max_angle': point.max_angle,'min_angle': point.min_angle, 'point_id': point.id})
            points.append(point_serialized)
        return Response(points)

    @action(methods=['get'], detail=True)
    def difficulties(self, request, pk=None):
        exercise = self.get_object()
        return Response(
            ExerciseDifficultySerializer(exercise.difficulties, many=True).data
        )

    @action(methods=['post'], detail=True)
    def post_difficulty(self, request, pk=None):
        exercise = self.get_object()
        if 'name' not in request.data or 'description' not in request.data or 'ranges' not in request.data or 'exercise_id' not in request.data:
            return Response(status=400)
        ranges = json.loads(request.data['ranges'])
        difficulty = ExerciseDifficulty.objects.create(
            exercise_id=int(request.data['exercise_id']),
            name=request.data['name'],
            description=request.data['description']
        )
        for range in ranges:
            DifficultyRange.objects.create(
                point_tracked_id=int(range['point_tracked']['point_id']),
                difficulty_id=difficulty.id,
                max_angle=range['max_angle'],
                min_angle=range['min_angle'],
            )
        return Response(status=201)