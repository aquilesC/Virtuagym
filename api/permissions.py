from rest_framework import permissions

from vg.models import Profile


class IsTrainer(permissions.BasePermission):
    """
    Custom permission to allow only owners of the endpoint to access it.
    """
    def has_permission(self, request, view):
        return request.user.profile.type_user == Profile.TRAINER