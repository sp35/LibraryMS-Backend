from rest_framework import permissions
from .models import Librarian, Student


class IsStudent(permissions.BasePermission):
    """
    Check if logged in user is student
    """

    def has_permission(self, request, view):
        return Student.objects.filter(auth_user=request.user).exists()


class IsLibrarian(permissions.BasePermission):
    """
    Check if logged in user is librarian
    """

    def has_permission(self, request, view):
        return Librarian.objects.filter(auth_user=request.user).exists()
