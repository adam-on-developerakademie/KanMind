from rest_framework.permissions import BasePermission

class IsBoardMemberOrOwner(BasePermission):
    """
    Permission: Nur Mitglieder oder Besitzer des Boards
    """
    
    def has_object_permission(self, request, view, obj):
        # Board-Owner hat immer Zugriff
        if obj.owner == request.user:
            return True
        
        # Board-Mitglieder haben Zugriff
        return obj.members.filter(id=request.user.id).exists()

class IsBoardOwner(BasePermission):
    """
    Permission: Nur der Besitzer des Boards
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
