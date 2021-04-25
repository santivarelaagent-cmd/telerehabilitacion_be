from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.therapy.models import ScheduledTrainingDifficulty
from telerehabilitation_API.therapy.serializers.scheduled_training_diff_serializer import \
    ScheduledTrainingDiffSerializer


class ScheduledTrainingDiffViewSet(APIView):
    def get(self, request):
        scheduled_training_id = request.GET.get('scheduled_training_id', 'NOT_FOUND')
        exercise_id = request.GET.get('exercise_id', 'NOT_FOUND')

        if scheduled_training_id != 'NOT_FOUND' and exercise_id != 'NOT_FOUND':
            return Response(
                ScheduledTrainingDiffSerializer(
                    ScheduledTrainingDifficulty.objects.filter(
                        scheduled_training_id=int(scheduled_training_id),
                        exercise_id=int(exercise_id)
                    ).first(),
                    context={'request': request}
                ).data,
                status=200
            )
        return Response(status=400)
