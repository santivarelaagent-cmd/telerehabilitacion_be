from django.db import models

from . import Routine


def upload_exercise_video_to(instance, filename):
    return 'exercise_{}/{}'.format(instance.id, filename)


class Exercise(models.Model):
    NO_VIDEO = "1"
    PROCESSING = "2"
    PROCESSED = "3"
    ERROR = "4"
    EXERCISE_STATUS = [
        (NO_VIDEO, "Sin video"),
        (PROCESSING, "Video en procesamiento"),
        (PROCESSED, "Video procesado"),
        (ERROR, "Error al procesar video")
    ]
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, related_name='exercises')
    name = models.CharField(max_length=128)
    description = models.TextField()
    order = models.IntegerField()
    video = models.URLField(max_length=512, blank=True, null=True)
    status = models.CharField(max_length=32, choices=EXERCISE_STATUS, default=NO_VIDEO)
    is_model = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
