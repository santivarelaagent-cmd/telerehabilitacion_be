from django.db import models

from telerehabilitation_API.therapy.models import SkeletonPoint, Exercise


class ExerciseSkeletonPointTracked(models.Model):
    skeleton_point = models.ForeignKey(SkeletonPoint, on_delete=models.SET_NULL, null=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True)
    max_angle = models.FloatField(null=True)
    min_angle = models.FloatField(null=True)
