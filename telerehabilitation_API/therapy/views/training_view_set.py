import pytz
from django.utils import timezone
from django.utils.timezone import localdate, localtime, now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.therapy.models import Training, ScheduledTraining
from telerehabilitation_API.therapy.serializers.training_serializer import TrainingSerializer


class TrainingViewSet(APIView):
    def get(self, request):
        training_id = request.GET.get('training_id', 'NOT_FOUND')
        scheduled_training_id = request.GET.get('scheduled_training_id', 'NOT_FOUND')
        if training_id != 'NOT_FOUND':
            try:
                return Response(
                    TrainingSerializer(
                        Training.objects.get(pk=int(training_id)),
                        context={'request': request}
                    ).data,
                    status=status.HTTP_200_OK
                )
            except Training.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)

        if scheduled_training_id != 'NOT_FOUND':
            try:
                return Response(
                    TrainingSerializer(
                        Training.objects.filter(schedule_training_id=int(scheduled_training_id)).first(),
                        context={'request': request}
                    ).data,
                    status=status.HTTP_200_OK
                )
            except Training.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)

        try:
            return Response(
                TrainingSerializer(
                    Training.objects.all(),
                    many=True,
                    context={'request': request}
                ).data,
                status=status.HTTP_200_OK
            )
        except Training.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            old_training = Training.objects.filter(schedule_training_id=request.data['schedule_training_id']).first()
            if old_training is None:
                raise Training.DoesNotExist()
            return Response({
                'id': old_training.id,
            }, status=status.HTTP_201_CREATED)
        except Training.DoesNotExist:
            new_training = Training.objects.create(
                schedule_training_id=request.data['schedule_training_id'],
                start_time=timezone.localtime(timezone.now(), pytz.timezone('America/Bogota'))
            )
            try:
                schedule_training = ScheduledTraining.objects.get(pk=request.data['schedule_training_id'])
                schedule_training.status = ScheduledTraining.STARTED
                schedule_training.save()
            except ScheduledTraining.DoesNotExist:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'id': new_training.id
            }, status=status.HTTP_201_CREATED)


class TrainingEndViewSet(APIView):
    def post(self, request):
        training_id = request.GET.get('training_id', 'NOT_FOUND')
        if training_id != 'NOT_FOUND':
            try:
                training = Training.objects.get(pk=int(training_id))
                training.end_time = timezone.localtime(timezone.now(), pytz.timezone('America/Bogota'))
                training.save()
                try:
                    schedule_training = ScheduledTraining.objects.get(pk=training.schedule_training_id)
                    schedule_training.status = ScheduledTraining.FINISHED
                    schedule_training.save()
                except ScheduledTraining.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
                return Response({}, status=status.HTTP_200_OK)
            except Training.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
