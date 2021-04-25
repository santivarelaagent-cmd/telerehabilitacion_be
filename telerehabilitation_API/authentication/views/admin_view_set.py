from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.authentication.models import Admin
from telerehabilitation_API.authentication.serializers.admin_serializer import AdminSerializer


class AdminViewSet(APIView):
    def get(self, request, format=None):
        return Response(AdminSerializer(Admin.objects.all(), many=True).data)

    def post(self, request):
        if 'username' not in request.data.keys() and \
           'email' not in request.data.keys() and \
           'first_name' not in request.data.keys() and \
           'last_name' not in request.data.keys():
            return Response({}, status=400)
        else:
            new_admin = User.objects.create_user(request.data['username'], request.data['email'], '123456789')
            new_admin.first_name = request.data['first_name']
            new_admin.last_name = request.data['last_name']
            new_admin.save()
            admin_group = Group.objects.get(name="Admin")
            admin_group.user_set.add(new_admin)
            Admin.objects.create(user_id=new_admin.id)
            return Response({}, status=201)

