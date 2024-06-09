from rest_framework import serializers
from api.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed



class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        model = User
        fields = ["email", "username" , "password","password2"]
        extra_kwargs = {"password": {"write_only": True}}
        
        
    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise serializers.ValidationError("Password must match")
        return data
    
    
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["email", "password"]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email", "name"]

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ["history"]