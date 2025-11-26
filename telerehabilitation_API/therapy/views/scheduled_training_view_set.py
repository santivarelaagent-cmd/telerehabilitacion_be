from datetime import datetime
import pytz

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers # Import serializers

from telerehabilitation_API.authentication.serializers import PatientSerializer, TherapistSerializer
from telerehabilitation_API.therapy.models import ScheduledTraining, ScheduledTrainingDifficulty, scheduled_training
from telerehabilitation_API.therapy.serializers import RoutineSerializer

# Define un Serializer auxiliar para la documentación de la respuesta del método GET
class ScheduledTrainingGetResponseBodySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, help_text="ID del entrenamiento programado")
    routine = RoutineSerializer(read_only=True, help_text="Detalles de la rutina asociada")
    start_time = serializers.DateTimeField(read_only=True, help_text="Hora de inicio del entrenamiento (zona horaria America/Bogota)")
    status = serializers.CharField(read_only=True, help_text="Código de estado del entrenamiento (ej. 'PENDING', 'COMPLETED')")
    status_verbose = serializers.CharField(read_only=True, help_text="Estado del entrenamiento legible para humanos")
    patient = PatientSerializer(read_only=True, required=False, help_text="Detalles del paciente (presente cuando se filtra por routine_id)")
    therapist = TherapistSerializer(read_only=True, required=False, help_text="Detalles del terapeuta (presente cuando se filtra por routine_id)")

# Define un Serializer para el cuerpo de la petición POST
class ScheduledTrainingPostRequestBodySerializer(serializers.Serializer):
    routine = serializers.IntegerField(help_text="ID de la rutina a programar")
    therapy_patient = serializers.IntegerField(help_text="ID del paciente de terapia al que se asigna el entrenamiento")
    start_time = serializers.CharField(help_text="Fecha y hora de inicio del entrenamiento (formato 'DD/MM/YYYY HH:MM:SS')")
    difficulties = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
            help_text="Lista de objetos de dificultad, cada uno con 'diff' (ID de dificultad) y 'exercise_id' (ID de ejercicio)"
        ),
        help_text="Lista de dificultades asociadas a ejercicios específicos para este entrenamiento"
    )

# Define un Serializer para la respuesta del método POST (vacía)
class ScheduledTrainingPostResponseBodySerializer(serializers.Serializer):
    # El método POST devuelve un objeto vacío en caso de éxito
    class Meta:
        ref_name = None # Evita que drf_yasg genere un nombre de referencia para un objeto vacío


class ScheduledTrainingViewSet(APIView):
    "This is a text description that help to explain this view"

    @swagger_auto_schema(
        operation_summary="Retrieve scheduled trainings",
        operation_description="""
        Retrieves a list of scheduled trainings or a single scheduled training instance.

        The behavior of this endpoint varies based on the provided query parameters:

        - **`patient_id`**: If provided, returns all scheduled trainings for that specific patient.
        - **`scheduled_training_id`**: If provided, returns the details of a single scheduled training.
        - **`routine_id`**: If provided, returns all scheduled trainings associated with a specific routine, including patient and therapist details.
        - **No parameters**: If no specific ID is provided, it returns all scheduled trainings for the currently authenticated user (patient).
        """,
        manual_parameters=[
            openapi.Parameter('routine_id', openapi.IN_QUERY, description="Filter by routine ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('scheduled_training_id', openapi.IN_QUERY, description="Get by scheduled training ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('patient_id', openapi.IN_QUERY, description="Filter by patient ID", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(
                description="Successful retrieval of scheduled training(s). Can be a list or a single object depending on query parameters.",
                schema=ScheduledTrainingGetResponseBodySerializer(many=True)
            ),
            404: "Not Found: No scheduled training(s) matching the criteria were found."
        }
    )
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

    @swagger_auto_schema(
        operation_summary="Create a new scheduled training",
        operation_description="Creates a new scheduled training instance with specified routine, patient, start time, and associated difficulties.",
        request_body=ScheduledTrainingPostRequestBodySerializer,
        responses={
            201: openapi.Response(
                description="Scheduled training created successfully.",
                schema=ScheduledTrainingPostResponseBodySerializer
            ),
            400: "Bad Request: Invalid data provided."
        }
    )
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
