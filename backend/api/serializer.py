from rest_framework import serializers
from api.models import User



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
        return User.objects.create_user(**validated_data)
    
    
class UserLoginSerializer(serializers.ModelSerializer):
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