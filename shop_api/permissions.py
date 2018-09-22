from rest_framework import permissions


class IsResourceOwnerOrReadOnly(permissions.BasePermission):

    """
    This permission class ensures that only the owner of a resource has the
    permission to modify its contents. It allows reading permissions
    to non-owners.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
