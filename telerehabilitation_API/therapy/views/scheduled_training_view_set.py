from datetime import datetime
import pytz

from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.authentication.serializers import PatientSerializer, TherapistSerializer
from telerehabilitation_API.therapy.models import ScheduledTraining, ScheduledTrainingDifficulty, scheduled_training
from telerehabilitation_API.therapy.serializers import RoutineSerializer


class ScheduledTrainingViewSet(APIView):
    def get(self, request):
        routine_id = request.GET.get('routine_id', 'NOT_FOUND')
        scheduled_training_id = request.GET.get('scheduled_training_id', 'NOT_FOUND')
        patient_id = request.GET.get('patient_id', 'NOT_FOUND')

        if patient_id != 'NOT_FOUND':
            try:
                scheduled_trainings = ScheduledTraining.objects.filter(therapy_patient_id=int(patient_id)).all()
                if scheduled_trainings:

                    return Response([{
                        'id': scheduled_training.id,
                        'routine': RoutineSerializer(scheduled_training.routine, context={'request': request}).data,
                        'start_time': scheduled_training.start_time.astimezone(pytz.timezone('America/Bogota')),
                        'status': scheduled_training.status,
                        'status_verbose': next(status[1] for status in ScheduledTraining.SCHEDULED_TRAINING_STATUS if
                                               status[0] == scheduled_training.status)
                    } for scheduled_training in scheduled_trainings], status=200)
                else:
                    return Response(status=404)
            except ScheduledTraining.DoesNotExist:
                return Response(status=404)

        if scheduled_training_id != 'NOT_FOUND':
            try:
                scheduled_training = ScheduledTraining.objects.get(pk=int(scheduled_training_id))
                if scheduled_training:

                    return Response({
                        'id': scheduled_training.id,
                        'routine': RoutineSerializer(scheduled_training.routine, context={'request': request}).data,
                        'start_time': scheduled_training.start_time.astimezone(pytz.timezone('America/Bogota')),
                        'status': scheduled_training.status,
                        'status_verbose': next(status[1] for status in ScheduledTraining.SCHEDULED_TRAINING_STATUS if
                                               status[0] == scheduled_training.status)
                    }, status=200)
                else:
                    return Response(status=404)
            except ScheduledTraining.DoesNotExist:
                return Response(status=404)

        if routine_id != 'NOT_FOUND':
            try:
                scheduled_trainings = ScheduledTraining.objects.filter(routine__id=routine_id).all()
                if scheduled_trainings:
                    return Response([{
                        'id': scheduled_training.id,
                        'routine': RoutineSerializer(scheduled_training.routine, context={'request': request}).data,
                        'start_time': scheduled_training.start_time.astimezone(pytz.timezone('America/Bogota')),
                        'patient': PatientSerializer(scheduled_training.therapy_patient.patient, context={'request': request}).data,
                        'therapist': TherapistSerializer(scheduled_training.therapy_patient.therapist, context={'request': request}).data,
                    } for scheduled_training in scheduled_trainings], status=200)
                else:
                    return Response(status=404)
            except ScheduledTraining.DoesNotExist:
                return Response(status=404)

        try:
            scheduled_trainings = ScheduledTraining.objects.filter(
                therapy_patient__patient__user_id=request.user.id).all()
            if scheduled_trainings:

                return Response([{
                    'id': scheduled_training.id,
                    'routine': RoutineSerializer(scheduled_training.routine, context={'request': request}).data,
                    'start_time': scheduled_training.start_time.astimezone(pytz.timezone('America/Bogota')),
                    'status': scheduled_training.status
                } for scheduled_training in scheduled_trainings], status=200)
            else:
                return Response(status=404)
        except ScheduledTraining.DoesNotExist:
            return Response(status=404)

    def post(self, request):
        body = request.data
        scheduled_training_obj = ScheduledTraining.objects.create(
            routine_id=body['routine'],
            therapy_patient_id=body['therapy_patient'],
            start_time=datetime.strptime(body['start_time']+':-0500', '%d/%m/%Y %H:%M:%S:%z')
        )
        for diff in request.data['difficulties']:
            ScheduledTrainingDifficulty.objects.create(
                difficulty_id=diff['diff'],
                exercise_id=diff['exercise_id'],
                scheduled_training= scheduled_training_obj
            )

        return Response({}, status=201)
