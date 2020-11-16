from django.db import models

from telerehabilitation_API.therapy.models import Routine, TherapyPatient


class ScheduledTraining(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, related_name='scheduled_trainings')
    therapy_patient = models.ForeignKey(
        TherapyPatient,
        on_delete=models.SET_NULL,
        null=True,
        related_name='therapy_patients'
    )
    start_time = models.DateTimeField(null=False)
    active = models.BooleanField(default=True)
