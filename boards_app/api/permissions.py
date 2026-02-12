from rest_framework.permissions import BasePermission

class IsBoardMemberOrOwner(BasePermission):
    """
    Permission: Only board members or owner
    """
    
    def has_object_permission(self, request, view, obj):
        # Board owner always has access
        if obj.owner == request.user:
            return True
        
        # Board members have access
        return obj.members.filter(id=request.user.id).exists()

class IsBoardOwner(BasePermission):
    """
    Permission: Only the board owner
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
