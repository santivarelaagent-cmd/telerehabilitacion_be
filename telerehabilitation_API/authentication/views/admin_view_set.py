from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.authentication.models import Admin
from telerehabilitation_API.authentication.serializers.admin_serializer import AdminSerializer


class AdminViewSet(APIView):
    def get(self, request, format=None):
        return Response(AdminSerializer(Admin.objects.all(), many=True).data)
