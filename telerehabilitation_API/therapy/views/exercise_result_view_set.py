import json

import pytz
import requests
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.therapy.models import ExerciseResult, ExerciseSkeletonPointTracked
from telerehabilitation_API.therapy.models.exercise_result_point import ExerciseResultPoint
from telerehabilitation_API.therapy.serializers import ExerciseSerializer
from telerehabilitation_API.therapy.serializers.exercise_results_serializer import ExerciseResultSerializer
from telerehabilitation_API.therapy.serializers.exercise_results_video_serializer import ExerciseResultsVideoSerializer
from drf_yasg.utils import swagger_auto_schema


class ExerciseResultViewSet(APIView):

    @swagger_auto_schema(
        operation_description="",
        operation_summary="",
        responses={200: ExerciseResultSerializer}
    )
    def get(self, request):
        exercise_result_id = request.GET.get('exercise_result_id', 'NOT_FOUND')
        training_id = request.GET.get('training_id', 'NOT_FOUND')
        if exercise_result_id != 'NOT_FOUND':
            try:
                return Response(
                    ExerciseResultSerializer(
                        ExerciseResult.objects.get(pk=int(exercise_result_id)),
                        context={'request': request}
                    ).data,
                    status=status.HTTP_200_OK
                )
            except ExerciseResult.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)

        if training_id != 'NOT_FOUND':
            try:
                return Response(
                    ExerciseResultSerializer(
                        ExerciseResult.objects.filter(training_id=training_id).all(),
                        many=True,
                        context={'request': request}
                    ).data,
                    status=status.HTTP_200_OK
                )
            except ExerciseResult.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)

        try:
            return Response(
                ExerciseResultSerializer(
                    ExerciseResult.objects.all(),
                    many=True,
                    context={'request': request}
                ).data,
                status=status.HTTP_200_OK
            )
        except ExerciseResult.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
    @swagger_auto_schema(
        request_body=ExerciseResultsVideoSerializer,
        responses={200: 'OK'}
    )
    def post(self, request):
        video_serialized = ExerciseResultsVideoSerializer(data=request.data)
        errors = []
        if not video_serialized.is_valid():
            errors.append({'video': video_serialized.error_messages})
        if 'training_id' not in request.data:
            errors.append({'training_id': 'There is no training_id'})
        if 'exercise_id' not in request.data:
            errors.append({'exercise_id': 'There is no exercise_id'})
        if not errors:
            new_exercise_result = ExerciseResult.objects.create(
                exercise_id=request.data['exercise_id'],
                training_id=request.data['training_id'],
                start_time=timezone.localtime(timezone.now(), pytz.timezone('America/Bogota'))
            )
            new_exercise_result.video = request.data['video']
            new_exercise_result.save()
            points_tracked = [{
                'center': x.skeleton_point.codename,
                'left_point': x.skeleton_point.left_point.codename,
                'right_point': x.skeleton_point.right_point.codename
            } for x in ExerciseSkeletonPointTracked.objects.filter(exercise=new_exercise_result.exercise).all()]
            try:
                send_video_response = requests.post(
                    'http://localhost:3000/video/',
                    files={'video': new_exercise_result.video},
                    data={
                        'points': json.dumps(points_tracked, separators=(',', ':')),
                        'exercise': json.dumps(
                            ExerciseSerializer(
                                new_exercise_result.exercise,
                                context={'request': request}
                            ).data,
                            separators=(',', ':')),
                        'resultsEndpoint': 'http://localhost:8000/exercise_results/{}/results'.format(
                            new_exercise_result.id)
                    }
                )
                if send_video_response.status_code == 200:
                    new_exercise_result.status = ExerciseResult.PROCESSING
                else:
                    new_exercise_result.status = ExerciseResult.ERROR
                new_exercise_result.save()
            except Exception as e:
                new_exercise_result.status = ExerciseResult.ERROR
                new_exercise_result.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)


class ExerciseResultResultsViewSet(APIView):
    def post(self, request, exercise_result_id):
        if 'error' not in request.data or 'results' not in request.data or not exercise_result_id:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        try:
            exercise_result = ExerciseResult.objects.get(pk=exercise_result_id)
            if request.data['error']:
                exercise_result.status = ExerciseResult.ERROR
                exercise_result.save()
            else:
                exercise_result.status = ExerciseResult.PROCESSED
                exercise_result.save()
                recieved_data = request.data['results']
                points = recieved_data['points']
                for point_tracked in ExerciseSkeletonPointTracked.objects.filter(
                        exercise=exercise_result.exercise).all():
                    point = next(x for x in points if x['center'] == point_tracked.skeleton_point.codename)
                    exercise_result_point = ExerciseResultPoint.objects.create(
                        point_tracked=point_tracked,
                        exercise_result=exercise_result
                    )
                    exercise_result_point.max_angle = float(point['max_angle'])
                    exercise_result_point.min_angle = float(point['min_angle'])
                    exercise_result_point.save()
            return Response(status=200)
        except ExerciseResult.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ExerciseResultConceptViewSet(APIView):
    def post(self, request, exercise_result_id):
        if 'concept' not in request.data:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        try:
            exercise_result = ExerciseResult.objects.get(pk=exercise_result_id)
            exercise_result.concept = request.data['concept']
            exercise_result.save()
            return Response(status=201)
        except ExerciseResult.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
