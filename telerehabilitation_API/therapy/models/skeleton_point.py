from django.db import models


class SkeletonPoint(models.Model):
    codename = models.CharField(max_length=64)
    verbose = models.CharField(max_length=128)
    left_point = models.ForeignKey('SkeletonPoint', on_delete=models.CASCADE, null=True, related_name='center_point_left')
    right_point = models.ForeignKey('SkeletonPoint', on_delete=models.CASCADE, null=True, related_name='center_point_right')
