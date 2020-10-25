from django.contrib.auth.models import User
from rest_framework import serializers


class UserModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email']
