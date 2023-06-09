from rest_framework import permissions
from rest_framework.permissions import BasePermission
from app.models import (User, )

class AllowRoles(BasePermission):
    """
    Custom permission to not allow actions on a serializer.
    This persmission looks for the DisableActions list on the serializer class.
    """
    def has_permission(self, request, view):
        if hasattr(view, 'allowed_roles'):
            for x in view.allowed_roles:
                if hasattr(request.user, x) and eval(f"request.user.{x}.is_role_active"):
                    return True
        return False

class DisableActionsPermission(BasePermission):
    """
    Custom permission to not allow actions on a serializer.
    This persmission looks for the DisableActions list on the serializer class.
    """
    def has_permission(self, request, view):
        print("inside dis per")
        if hasattr(view, 'disable_actions'):
            if request.user.is_superuser:
                return True

            if request.method in view.disable_actions:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        print("inside obj dis per")
        if hasattr(view, 'disable_actions'):
            if request.user.is_superuser:
                return True

            if request.method in view.disable_actions:
                return False
        return True

class OnlyAdminActionsPermission(BasePermission):
    def has_permission(self, request, view):

        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True

        return hasattr(user, 'admin') and user.admin.is_role_active

class OnlyAdminPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return hasattr(user, 'admin') and user.admin.is_role_active

class OnlyStaffActionsPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff

class OnlyStaffPermission(BasePermission):
    def has_permission(self, request, view):

        return request.user.is_staff


class OwnerRequiredPermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """
    def has_permission(self, request, view):
        print("inside obj own per")
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #if request.user.is_superuser: return True
        print("inside obj own per")
        if request.user.is_superuser:
            return  True

        if request.method in permissions.SAFE_METHODS:
            return True

        # obj here is a UserProfile instance
        if isinstance(obj, User):
            return obj == request.user


class OwnerActionsPermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        print("inside owner actions")
        if request.method in ['POST']:
            return request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return  True

        if request.method in permissions.SAFE_METHODS:
            return True

        # obj here is a UserProfile instance
        if isinstance(obj, User):
            return obj == request.user



class AnonymousOnlyPOSTPermission(BasePermission):
    """
    Custom permission to not allow actions on a serializer.
    This persmission looks for the DisableActions list on the serializer class.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ['POST']:
            return request.user.is_anonymous

class AdminOnlyPOSTPermission(BasePermission):
    """
    Custom permission to not allow actions on a serializer.
    This persmission looks for the DisableActions list on the serializer class.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        print("inside admin only post")
        if request.method in ['POST']:
            return request.user.is_superuser
        return False



class UserViewPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return  True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['POST']:
            return request.user.is_anonymous

        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #if request.user.is_superuser: return True
        if request.user.is_superuser:
            return  True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH',]:
            return obj == request.user







class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

class StaffOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff

class OwnerOnly(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, User):
            return obj == request.user

        return False
