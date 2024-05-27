import re
from rest_framework import serializers
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True}
        }

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('The name is too short')
        return value

    def create(self, validated_data):
        validated_data['name'] = self.validate_name(validated_data.get('name'))
        return User.objects.create_user(**validated_data)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    action = serializers.ChoiceField(choices=['reset', 'verify'])


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_password(self, value):
        if not self.is_valid_password(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase "
                "letter, and one digit")
        return value

    def validate_confirm_password(self, value):
        if not self.is_valid_password(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase "
                "letter, and one digit")
        return value

    def is_valid_password(self, value):
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', value))

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm_password do not match")
        return data
