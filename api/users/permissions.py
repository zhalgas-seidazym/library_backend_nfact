from rest_framework import permissions


class IsVerifiedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        elif not request.user.verified:
            raise permissions.exceptions.PermissionDenied("You have not verified your email")
        else:
            return True
