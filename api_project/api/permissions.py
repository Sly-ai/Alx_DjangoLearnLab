from rest_framework.permissions import BasePermission

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to only allow authenticated users to edit objects.
    Unauthenticated users can only read (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_authenticated