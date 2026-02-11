from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import models
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, TaskCreateUpdateSerializer, CommentSerializer
from .permissions import IsTaskBoardMember, IsTaskCreatorOrBoardOwner, IsCommentAuthor

class TaskAssignedToMeView(APIView):
    """
    GET /api/tasks/assigned-to-me/
    Tasks die mir zugewiesen sind
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskReviewingView(APIView):
    """
    GET /api/tasks/reviewing/
    Tasks die ich reviewen soll
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskCreateView(APIView):
    """
    POST /api/tasks/
    Task erstellen
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = TaskCreateUpdateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            # Prüfen ob User Mitglied des Boards ist
            board = serializer.validated_data['board']
            if not (board.owner == request.user or 
                   board.members.filter(id=request.user.id).exists()):
                return Response(
                    {'error': 'Keine Berechtigung für dieses Board'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            task = serializer.save()
            response_serializer = TaskSerializer(task)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    """
    PATCH/DELETE /api/tasks/{task_id}/
    Task aktualisieren oder löschen
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, task_id):
        """Task-Objekt abrufen"""
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None
    
    def patch(self, request, task_id):
        """Task aktualisieren"""
        task = self.get_object(task_id)
        if not task:
            return Response(
                {'error': 'Task nicht gefunden'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Permission prüfen
        board = task.board
        if not (board.owner == request.user or 
               board.members.filter(id=request.user.id).exists()):
            return Response(
                {'error': 'Keine Berechtigung'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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
        """Task löschen"""
        task = self.get_object(task_id)
        if not task:
            return Response(
                {'error': 'Task nicht gefunden'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Permission prüfen (nur Ersteller oder Board-Owner)
        if not (task.created_by == request.user or task.board.owner == request.user):
            return Response(
                {'error': 'Keine Berechtigung zum Löschen'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskCommentsView(APIView):
    """
    GET/POST /api/tasks/{task_id}/comments/
    Kommentare abrufen oder erstellen
    """
    permission_classes = [IsAuthenticated]
    
    def get_task(self, task_id):
        """Task-Objekt abrufen"""
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None
    
    def get(self, request, task_id):
        """Kommentare abrufen"""
        task = self.get_task(task_id)
        if not task:
            return Response(
                {'error': 'Task nicht gefunden'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Permission prüfen
        board = task.board
        if not (board.owner == request.user or 
               board.members.filter(id=request.user.id).exists()):
            return Response(
                {'error': 'Keine Berechtigung'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, task_id):
        """Kommentar erstellen"""
        task = self.get_task(task_id)
        if not task:
            return Response(
                {'error': 'Task nicht gefunden'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Permission prüfen
        board = task.board
        if not (board.owner == request.user or 
               board.members.filter(id=request.user.id).exists()):
            return Response(
                {'error': 'Keine Berechtigung'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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
    Kommentar löschen
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, task_id, comment_id):
        """Kommentar löschen"""
        try:
            comment = Comment.objects.get(id=comment_id, task_id=task_id)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Kommentar nicht gefunden'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Permission prüfen (nur Autor)
        if comment.author != request.user:
            return Response(
                {'error': 'Keine Berechtigung zum Löschen'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)