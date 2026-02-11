from rest_framework.permissions import BasePermission

class IsTaskBoardMember(BasePermission):
    """
    Permission: Nur Mitglieder des Boards der Task
    """
    
    def has_object_permission(self, request, view, obj):
        board = obj.board
        
        # Board-Owner hat immer Zugriff
        if board.owner == request.user:
            return True
        
        # Board-Mitglieder haben Zugriff
        return board.members.filter(id=request.user.id).exists()

class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Permission: Nur Task-Ersteller oder Board-Besitzer
    """
    
    def has_object_permission(self, request, view, obj):
        # Task-Ersteller hat Zugriff
        if obj.created_by == request.user:
            return True
        
        # Board-Owner hat Zugriff
        return obj.board.owner == request.user

class IsCommentAuthor(BasePermission):
    """
    Permission: Nur Kommentar-Autor
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
