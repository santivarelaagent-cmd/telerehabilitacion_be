from django.contrib.auth.models import User
from rest_framework import serializers

from telerehabilitation_API.auth.serializers.group_serializer import GroupSerializer


class UserModelSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'groups']
