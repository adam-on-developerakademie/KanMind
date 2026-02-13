from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import AllowAny
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
    

