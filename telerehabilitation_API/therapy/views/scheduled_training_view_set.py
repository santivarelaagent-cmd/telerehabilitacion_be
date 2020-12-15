from datetime import datetime
import pytz

from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.therapy.models import ScheduledTraining
from telerehabilitation_API.therapy.serializers import RoutineSerializer


class ScheduledTrainingViewSet(APIView):
    def get(self, request):
        try:
            scheduled_trainings = ScheduledTraining.objects.filter(therapy_patient__patient__user_id=request.user.id).all()
            if scheduled_trainings:

                return Response([{
                    'routine': RoutineSerializer(scheduled_training.routine, context={'request': request}).data,
                    'start_time': scheduled_training.start_time.astimezone(pytz.timezone('America/Bogota'))
                } for scheduled_training in scheduled_trainings], status=200)
            else:
                return Response(status=404)
        except ScheduledTraining.DoesNotExist:
            return Response(status=404)

    def post(self, request):
        body = request.data
        print(body['start_time'])
        ScheduledTraining.objects.create(
            routine_id=body['routine'],
            therapy_patient_id=body['therapy_patient'],
            start_time=datetime.strptime(body['start_time']+':-0500', '%d/%m/%Y %H:%M:%S:%z')
        )
        return Response({}, status=201)
