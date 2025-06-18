from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                "error": "Username and password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({
                "error": "User with this username does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "message": "User logged in successfully."
            })
        else:
            return Response({
                "error": "Incorrect password."
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)