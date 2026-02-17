from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from auth_app.api.serializers import UserSerializer
from boards_app.models import Board
from .serializers import (
    BoardListSerializer, 
    BoardDetailSerializer, 
    BoardCreateUpdateSerializer,
    BoardUpdateSerializer
)
from .permissions import IsBoardMemberOrOwner, IsBoardOwner

User = get_user_model()

class BoardViewSet(ModelViewSet):
    """
    ViewSet for Board CRUD operations
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Different serializer per action"""
        if self.action == 'list':
            return BoardListSerializer
        elif self.action == 'retrieve':
            return BoardDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return BoardUpdateSerializer
        return BoardCreateUpdateSerializer
    
    def get_permissions(self):
        """Different permissions per action"""
        if self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsBoardOwner]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Only boards user is allowed to see"""
        #print(f"get_queryset called for user: {self.request.user}")  # Debug
        user = self.request.user
        return Board.objects.filter(
            models.Q(owner=user) | models.Q(members=user)
        ).distinct()
    
    def get_object(self):
        """Get object and return 403 instead of 404 if no permission"""
        pk = self.kwargs.get('pk')
        
        # First check if board exists at all
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            # Board doesn't exist - return 404
            raise get_object_or_404(Board, pk=pk)
        
        # Board exists, check permissions  
        user = self.request.user
        if not (board.owner == user or board.members.filter(id=user.id).exists()):
            # Board exists but no permission - return 403
            raise PermissionDenied("You don't have permission to access this board")
        
        return board

class EmailCheckView(APIView):
    """
    GET /api/email-check/?email=example@mail.com
    Checks if email exists
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        email = request.query_params.get('email')
        
        if not email:
            return self._email_missing_error()
        
        user = self._find_user_by_email(email)
        if not user:
            return self._email_not_found_error()
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def _email_missing_error(self):
        """Return for missing email parameter"""
        return Response(
            {'error': 'Email parameter missing'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def _find_user_by_email(self, email):
        """Search user by email"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    def _email_not_found_error(self):
        """Return for email not found"""
        return Response(
            {'error': 'Email not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

