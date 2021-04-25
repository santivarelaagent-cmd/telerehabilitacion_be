from django.db import models

from . import Exercise
from .training import Training


def upload_exercise_video_to(instance, filename):
    return 'exercise_result_{}/{}'.format(instance.id, filename)


class ExerciseResult(models.Model):
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
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True, related_name='results')
    training = models.ForeignKey(Training, on_delete=models.SET_NULL, null=True, related_name='results')
    start_time = models.DateTimeField(null=True)
    video = models.FileField(upload_to=upload_exercise_video_to)
    status = models.CharField(max_length=32, choices=EXERCISE_STATUS, default=NO_VIDEO)
    concept = models.TextField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
