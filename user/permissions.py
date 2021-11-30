from rest_framework.permissions import SAFE_METHODS, BasePermission


class AllowAny(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True
        
        return obj.id == request.user.id


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        return obj.id == request.user.id