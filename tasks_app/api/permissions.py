from rest_framework.permissions import BasePermission

class IsTaskBoardMember(BasePermission):
    """
    Permission: Only board members of the task
    """
    
    def has_object_permission(self, request, view, obj):
        board = obj.board
        
        # Board owner always has access
        if board.owner == request.user:
            return True
        
        # Board members have access
        return board.members.filter(id=request.user.id).exists()

class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Permission: Only task creator or board owner
    """
    
    def has_object_permission(self, request, view, obj):
        # Task creator has access
        if obj.created_by == request.user:
            return True
        
        # Board owner has access
        return obj.board.owner == request.user

class IsCommentAuthor(BasePermission):
    """
    Permission: Only comment author
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
