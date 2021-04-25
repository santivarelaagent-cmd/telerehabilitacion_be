from rest_framework import permissions


class IsAdminTherapistOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        for group in request.user.groups.all():
            print(group.name)
            if group.name == 'Admin' or group.name == 'Therapist':
                return True

        return False
