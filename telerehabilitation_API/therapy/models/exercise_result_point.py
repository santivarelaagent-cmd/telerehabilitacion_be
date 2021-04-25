from django.db import models

from telerehabilitation_API.therapy.models import ExerciseSkeletonPointTracked, ExerciseResult


class ExerciseResultPoint(models.Model):
    point_tracked = models.ForeignKey(ExerciseSkeletonPointTracked, on_delete=models.SET_NULL, null=True)
    max_angle = models.FloatField(null=True)
    min_angle = models.FloatField(null=True)
    exercise_result = models.ForeignKey(ExerciseResult, on_delete=models.SET_NULL, null=True, related_name='points')
    score = models.PositiveIntegerField(null=True, blank=True)
