from rest_framework import serializers
from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):

     class Meta:
         model = CustomUser
         fields = ('email', 'username', 'password')
         extra_kwargs = {'password':{'write_only':True}}

     def validate_password(self, value):
         if len(value) < 6:
             raise serializers.ValidationError("Password must be at least 6 characters.")
         return value

     def create(self, validated_data):
         return CustomUser.objects.create_user(**validated_data)
