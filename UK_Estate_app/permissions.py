from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group


class IsNotDefaultGroupUser(BasePermission):
    """
    Allows access only to users who are not in the 'Default' group.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='CanSubmitInquiry').exists()