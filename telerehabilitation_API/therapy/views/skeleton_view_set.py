from rest_framework import permissions, viewsets, pagination

from telerehabilitation_API.therapy.models import SkeletonPoint
from telerehabilitation_API.therapy.serializers import SkeletonPointSerializer


class SkeletonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SkeletonPoint.objects.all()
    serializer_class = SkeletonPointSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination.PageNumberPagination.page_size = 100
