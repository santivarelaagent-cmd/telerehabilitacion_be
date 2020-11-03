from django.db import models

from . import Routine


class Exercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, related_name='exercises')
    name = models.CharField(max_length=128)
    description = models.TextField()
    order = models.IntegerField()
    video = models.FileField()
    has_been_tracked = models.BooleanField(default=False)
    is_model = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
