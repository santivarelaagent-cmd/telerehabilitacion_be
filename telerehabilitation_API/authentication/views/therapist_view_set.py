from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.authentication.models import Therapist
from telerehabilitation_API.authentication.serializers import TherapistSerializer


class TherapistViewSet(APIView):
    def get(self, request, format=None):
        return Response(TherapistSerializer(Therapist.objects.all(), many=True).data)
