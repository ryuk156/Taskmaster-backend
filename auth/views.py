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
    if 'username' not in request.data or 'password' not in request.data:
        # Check if both username and password are provided
        return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    user = authenticate(username=request.data['username'], password=request.data['password'])

    if user is None:
        # If authentication fails (either username or password is incorrect)
        return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate or retrieve token for the authenticated user
    token, created = Token.objects.get_or_create(user=user)

    # Serialize user data (to send to the client)
    serializer = UserSerializer(instance=user)

    # Return the token and user details
    return Response({
        "token": token.key,
        "user": serializer.data,
        "status": status.HTTP_200_OK,
        "message": "Login successful"
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def UserLogout(request):
    if request.method == 'GET':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    




        
    
