from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from searilizer import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


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
        token = get_tokens_for_user(user)
        return {'token':token,'msg':'User Registration success'}, status.HTTP_201_CREATED
    return serializer.errors, status.HTTP_400_BAD_REQUEST


@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email= serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return {'token':token,'msg':'Login Successful'}, status.HTTP_201_CREATED
        return {'msg':'Login Failed'}, status.HTTP_400_BAD_REQUEST
    return serializer.errors, status.HTTP_400_BAD_REQUEST


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