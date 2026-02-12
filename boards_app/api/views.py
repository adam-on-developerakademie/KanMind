from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth import get_user_model
from boards_app.models import Board
from auth_app.api.serializers import UserSerializer
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
    ViewSet für Board CRUD-Operationen
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Verschiedene Serializer je nach Action"""
        if self.action == 'list':
            return BoardListSerializer
        elif self.action == 'retrieve':
            return BoardDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return BoardUpdateSerializer
        return BoardCreateUpdateSerializer
    
    def get_permissions(self):
        """Verschiedene Permissions je nach Action"""
        if self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsBoardOwner]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Nur Boards die der User sehen darf"""
        user = self.request.user
        return Board.objects.filter(
            models.Q(owner=user) | models.Q(members=user)
        ).distinct()

class EmailCheckView(APIView):
    """
    GET /api/email-check/?email=example@mail.com
    Prüft ob E-Mail existiert
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
        """Rückgabe für fehlenden E-Mail Parameter"""
        return Response(
            {'error': 'E-Mail Parameter fehlt'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def _find_user_by_email(self, email):
        """Benutzer nach E-Mail suchen"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    def _email_not_found_error(self):
        """Rückgabe für nicht gefundene E-Mail"""
        return Response(
            {'error': 'E-Mail nicht gefunden'}, 
            status=status.HTTP_404_NOT_FOUND
        )
            
