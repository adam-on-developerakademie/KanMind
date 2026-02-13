from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import models
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, TaskCreateUpdateSerializer, CommentSerializer
from .permissions import IsTaskBoardMember, IsTaskCreatorOrBoardOwner, IsCommentAuthor


class TaskBaseView(APIView):
    """
    Base class for Task views with shared functionality
    """
    permission_classes = [IsAuthenticated]
    
    def get_task_or_permission_denied(self, task_id):
        """Get task object or return permission denied for security"""
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {'error': 'No permission'}, 
                status=status.HTTP_403_FORBIDDEN
            )
    
    def check_board_permission(self, user, board):
        """Check board permission"""
        return (board.owner == user or 
                board.members.filter(id=user.id).exists())
    
    def get_permission_error(self):
        """Standard permission error"""
        return Response(
            {'error': 'No permission'}, 
            status=status.HTTP_403_FORBIDDEN
        )

class TaskAssignedToMeView(APIView):
    """
    GET /api/tasks/assigned-to-me/
    Tasks assigned to me
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskReviewingView(APIView):
    """
    GET /api/tasks/reviewing/
    Tasks I should review
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskCreateView(TaskBaseView):
    """
    POST /api/tasks/
    Create task
    """
    def post(self, request):
        serializer = TaskCreateUpdateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not self._check_create_permission(request, serializer.validated_data['board']):
            return self.get_permission_error()
        
        task = serializer.save()
        response_serializer = TaskSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def _check_create_permission(self, request, board):
        """Check creation permission for board"""
        return self.check_board_permission(request.user, board)

class TaskDetailView(TaskBaseView):
    """
    PATCH/DELETE /api/tasks/{task_id}/
    Update or delete task
    """
    def patch(self, request, task_id):
        task = self.get_task_or_permission_denied(task_id)
        if isinstance(task, Response):  # Error Response
            return task
        
        if not self.check_board_permission(request.user, task.board):
            return self.get_permission_error()
        
        return self._update_task(request, task)
    
    def _update_task(self, request, task):
        """Task update logic"""
        serializer = TaskCreateUpdateSerializer(
            task,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            updated_task = serializer.save()
            response_serializer = TaskSerializer(updated_task)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id):
        task = self.get_task_or_permission_denied(task_id)
        if isinstance(task, Response):  # Error Response
            return task
        
        if not self._check_delete_permission(request.user, task):
            return self.get_permission_error()
        
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def _check_delete_permission(self, user, task):
        """Check delete permission"""
        return (task.created_by == user or task.board.owner == user)

class TaskCommentsView(TaskBaseView):
    """
    GET/POST /api/tasks/{task_id}/comments/
    Get or create comments
    """
    def get(self, request, task_id):
        task = self.get_task_or_permission_denied(task_id)
        if isinstance(task, Response):  # Error Response
            return task
        
        if not self.check_board_permission(request.user, task.board):
            return self.get_permission_error()
        
        return self._get_comments_response(task)
    
    def _get_comments_response(self, task):
        """Get comments and create response"""
        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, task_id):
        task = self.get_task_or_permission_denied(task_id)
        if isinstance(task, Response):  # Error Response
            return task
        
        if not self.check_board_permission(request.user, task.board):
            return self.get_permission_error()
        
        return self._create_comment(request, task)
    
    def _create_comment(self, request, task):
        """Comment creation logic"""
        serializer = CommentSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            comment = serializer.save(task=task)
            return Response(
                CommentSerializer(comment).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    """
    DELETE /api/tasks/{task_id}/comments/{comment_id}/
    Delete comment
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, task_id, comment_id):
        comment = self._get_comment_or_permission_denied(task_id, comment_id)
        if isinstance(comment, Response):  # Error Response
            return comment
        
        if not self._check_author_permission(request.user, comment):
            return Response(
                {'error': 'No permission to delete'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def _get_comment_or_permission_denied(self, task_id, comment_id):
        """Get comment or return permission denied for security"""
        try:
            return Comment.objects.get(id=comment_id, task_id=task_id)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'No permission'}, 
                status=status.HTTP_403_FORBIDDEN
            )
    
    def _check_author_permission(self, user, comment):
        """Check if user is the author"""
        return comment.author == user