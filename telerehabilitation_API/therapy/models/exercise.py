from django.db import models

from . import Routine


def upload_exercise_video_to(instance, filename):
    return 'exercise_{}/{}'.format(instance.id, filename)


class Exercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, related_name='exercises')
    name = models.CharField(max_length=128)
    description = models.TextField()
    order = models.IntegerField()
    video = models.FileField(upload_to=upload_exercise_video_to)
    has_been_tracked = models.BooleanField(default=False)
    is_model = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
