from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit/delete their objects.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions: only author can update/delete
        return getattr(obj, 'author', None) == request.user
