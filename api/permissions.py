from django.contrib.auth import get_user_model

from rest_framework import permissions
from library.models import BorrowRecord


User = get_user_model()


class IsOwner(permissions.BasePermission):
    """
    Grants access to the owner of an object.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return request.user == obj
        elif isinstance(obj, BorrowBook):
            return request.user == obj.user

        return False


class IsLibrarian(permissions.BasePermission):
    """
    Grants access to a librarian.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == User.Role.LIBRARIAN
        )


class IsNotAuthenticated(permissions.BasePermission):
    """
    Grants access to unauthenticated viewers.
    """
    def has_permission(self, request, view):
        return not request.user.is_authenticated
