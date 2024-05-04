from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from auth.serializers import UserSerializer

# Create your views here.
@api_view(['POST'])
def UserRegister(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user object first
            user.set_password(request.data['password'])  # Set password separately
            user.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
def UserLogin(request):
    if request.method == 'POST':
        # Check if 'username' and 'password' are provided in the request data
        if 'username' not in request.data or 'password' not in request.data:
            return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user based on provided username and password
        user = authenticate(username=request.data['username'], password=request.data['password'])

        if user is None:
            # If user is not authenticated (username or password is incorrect)
            return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate or retrieve token
        token, created = Token.objects.get_or_create(user=user)

        # Serialize user data
        serializer = UserSerializer(instance=user)

        # Return token and user details
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        # Check if 'username' and 'password' are provided in the request data
        if 'username' not in request.data or 'password' not in request.data:
            return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, username=request.data['username'])
        except User.DoesNotExist:
            # If user with provided username doesn't exist
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the password matches
        if not user.check_password(request.data['password']):
            # If password doesn't match
            return Response({"message": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate or retrieve token
        token, created = Token.objects.get_or_create(user=user)

        # Serialize user data
        serializer = UserSerializer(instance=user)

        # Return token and user details
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def UserLogout(request):
    if request.method == 'GET':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
        
    
