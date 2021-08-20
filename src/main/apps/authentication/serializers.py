from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.signals import user_logged_in
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from typing import (
    Generic,
    List,
    TypeVar,
)
InputDataDict = TypeVar('InputDataDict')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'is_verified')


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'is_verified', 'created_at', 'first_name', 'last_name')


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[
        validate_password], style={'input_type': 'password', })
    password2 = serializers.CharField(write_only=True, required=True, style={
        'input_type': 'password', })

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True},
                        'password2': {'write_only': True}, }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        user = User.objects.get(username=instance.username)
        Token.objects.create(user=user)
        return instance

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return data

    def update(self, instance, validated_data):
        for data, value in validated_data.items():
            if data == 'password':
                instance.set_password(value)
            else:
                setattr(instance, data, value)
        instance.save()
        return instance


class SignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, style={'input_type': 'password', })

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data: Generic[InputDataDict]) -> User:
        user = authenticate(**data)
        # Banned or disabled user.
        if not user and User.objects.filter(username=data['username']).count() > 0:
            raise serializers.ValidationError("This account has been deactivated by an administrator.")
        if user:
            if not user.is_verified:
                raise serializers.ValidationError(
                    "This account has not been verified.")
            user_logged_in.send(sender=user.__class__, user=user)
            return user
        raise serializers.ValidationError("Incorrect credentials.")
