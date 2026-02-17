from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

User = get_user_model()

class RegistrationView(APIView):
    """
    POST /api/registration/
    Creates a new user
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'token': user.token,
                'fullname': user.fullname,
                'email': user.email,
                'user_id': user.id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    POST /api/login/
    Authenticates a user
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = {
                'token': serializer.validated_data['token'],
                'fullname': serializer.validated_data['fullname'],
                'email': serializer.validated_data['email'],
                'user_id': serializer.validated_data['user_id']
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
    """
    DELETE /api/users/{user_id}/
    Delete a user - only the user themselves or staff users allowed
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, user_id):
        user_to_delete = get_object_or_404(User, id=user_id)
        
        # Check permission: only the user themselves or staff users can delete
        if not self._check_delete_permission(request.user, user_to_delete):
            return Response(
                {'error': 'No permission to delete this user'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_to_delete.delete()
        return Response({'message': f'User {user_to_delete.fullname} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    def _check_delete_permission(self, requesting_user, user_to_delete):
        """Check if user has permission to delete"""
        return requesting_user == user_to_delete or requesting_user.is_staff
    

