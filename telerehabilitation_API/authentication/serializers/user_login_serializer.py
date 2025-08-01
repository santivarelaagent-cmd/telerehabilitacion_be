from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=0, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        print(data)
        user = authenticate(username=data['username'], password=data['password'])
        print(user)
        if not user:
            raise serializers.ValidationError('The credentials are not valid')

        self.context['user'] = user
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
