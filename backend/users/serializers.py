from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.USER_ROLES)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2", "role"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError({"password": "Password do no match"})

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
