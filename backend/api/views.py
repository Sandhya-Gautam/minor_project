from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializer import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # token = get_tokens_for_user(user)
        return Response({'msg': 'Registration Successful'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email= serializer.data.get('email')
        password = serializer.data.get('password')
        print("hello")
        user = authenticate(email=email,password=password)
 
        if user is not None:
            print("hello")
            # token = get_tokens_for_user(user)
            return Response({'msg':'Login Successful'}, status.HTTP_201_CREATED)
        return Response({'msg':'Login Failed'}, status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserProfileSerializer(request.user)
    return serializer.data, status.HTTP_200_OK

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    serializer = HistorySerializer(request.user)
    return serializer.data, status.HTTP_200_OK

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AskQSn(request):
    text=request.data
    
