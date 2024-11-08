from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.post_user.user == request.user
    

class IsAuthenticatedForPostOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.method == 'POST':
            return True
        
        return request.user.is_authenticated