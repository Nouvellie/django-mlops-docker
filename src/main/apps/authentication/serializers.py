import uuid

from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.signals import user_logged_in
from main.exceptions import CustomError
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from typing import (
    Dict,
    Generic,
    List,
    TypeVar,
)
from typing import (
    Generic,
    TypeVar,
)
API_INPUTS = TypeVar('API_INPUTS')

# HELP TEXT.
FASHION_MNIST_HELP_TEXT = f"Please enter an image to process with FashionMnist model. The filename cannot be longer than 50 characters and only .png format will be accepted."
IMDB_SENTIMENT_HELP_TEXT = f"Please enter a file or text (review) to be processed with the Imdb Sentiment model. The filename cannot be longer than 50 characters and the allowed formats are '.md, .txt, .docx'. (In case both parameters are sent, the file is validated first and only one is answered.)"
PASSWORD_HELP_TEXT = f"Please enter a file or text (code) to be processed with the Stackoverflow model. The filename cannot be longer than 50 characters and the allowed formats are '.md, .txt, .docx'. (In case both parameters are sent, the file is validated first and only one is answered.)"
CATS_VS_DOGS_HELP_TEXT = f"Please enter an image to process with CatsVsDogs model. The filename cannot be longer than 50 characters and only .jpg format will be accepted."


class UserSerializer(serializers.ModelSerializer):
    """Returns a modified serialized dictionary of the user model."""

    class Meta:
        model = User
        fields = ('username', 'email', 'is_verified',)


class UserInfoSerializer(serializers.ModelSerializer):
    """Returns a modified serialized info dictionary of the user model."""

    class Meta:
        model = User
        fields = ('username', 'email', 'is_verified',
                  'created_at', 'first_name', 'last_name',)


class SignUpSerializer(serializers.ModelSerializer):
    """This class serializes the creation of a new account, with all the validations are ok."""

    password = serializers.CharField(
        write_only=True,
        label="Password",
        validators=[validate_password],
        trim_whitespace=False,
        style={'input_type': 'password', }
    )
    password2 = serializers.CharField(
        write_only=True,
        label="Confirm Password",
        validators=[validate_password],
        trim_whitespace=False,
        style={'input_type': 'password', }
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2',)

    def create(self, validated_data: Generic[API_INPUTS]) -> User:
        """User creation."""
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)
        new_user = self.Meta.model(**validated_data)
        if password is not None:
            new_user.set_password(password)
        new_user.save()
        user = User.objects.get(username=new_user.username)
        Token.objects.create(user=user)
        return user

    def validate(self, attrs: Generic[API_INPUTS]) -> Generic[API_INPUTS]:
        """SignUp data validation."""
        if attrs['password'] != attrs['password2']:
            raise CustomError(detail="Password fields didn't match.", code=400)
        if attrs['username'] == attrs['password']:
            raise CustomError(
                detail="For your security the username and password cannot be the same.", code=403)
        if attrs['password'] == attrs['email'].split("@")[0]:
            raise CustomError(
                detail="For your security the email and password cannot be the same.", code=403)
        if attrs['password'].startswith(str(attrs['email'].split("@")[0][:4])):
            raise CustomError(
                detail="For your security, the password cannot contain your e-mail address.", code=403)
        if attrs['password'].startswith(str(attrs['username'][:4])):
            raise CustomError(
                detail="For your security, the password cannot contain your username.", code=403)
        if attrs['username'] == attrs['email'].split("@")[0]:
            raise CustomError(
                detail="For your security the username and email address cannot be the same.", code=403)
        # Validation @email.
        # if attrs['email'].split("@")[1].split(".")[0].lower() != 'nouvellie':
        #     raise CustomError(
        #         detail="The e-mail does not correspond to those allowed in the system.", code=403)
        return super().validate(attrs)


class SignInSerializer(serializers.ModelSerializer):
    """Validates the credentials of an account when signin."""

    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        label="Password",
        trim_whitespace=False,
        style={'input_type': 'password', }
    )

    class Meta:
        model = User
        fields = ('username', 'password',)

    def validate(self, attrs: Generic[API_INPUTS]) -> Generic[API_INPUTS]:
        """SignIn data validation."""
        user = authenticate(**attrs)
        if user:
            if user.is_active and user.is_verified:
                attrs.update({'user': user})
                return super().validate(attrs)
            elif user.is_active and not user.is_verified:
                raise CustomError(
                    detail="This account has not been verified.", code=403)
            elif not user.is_active:
                raise CustomError(
                    detail="This account has been deactivated by an administrator.", code=403)
        else:
            raise CustomError(detail="Incorrect credentials.", code=401)

    def get_user(self):
        """Return User."""
        return list(self.validated_data.items())[-1][1]


class TokenInfoSerializer(serializers.Serializer):

    token = serializers.CharField(
        label="Token", help_text="Token hash. (unique)")

    class Meta:
        fields = ('token',)


class AccountVerificationSerializer(serializers.ModelSerializer):

    acc_hash = serializers.CharField(
        write_only=True,
        label="Hash",
        help_text="Hash link sent to email."
    )

    class Meta:
        model = User
        fields = ('acc_hash',)

    def validate(self, attrs: Generic[API_INPUTS]) -> Generic[API_INPUTS]:
        """Hash validation."""
        acc_hash = attrs['acc_hash']
        if not User.objects.filter(acc_hash=acc_hash).exists():
            raise CustomError(
                detail="The verification link is invalid, please request a new one.", code=403)
        else:
            user = User.objects.get(acc_hash=acc_hash)
        if not user.is_active:
            raise CustomError(
                detail="This account cannot be verified because it has been deactivated by an administrator.", code=403)
        elif user.is_verified:
            raise CustomError(
                detail="This account has already been verified.", code=208)
        else:
            user.is_verified = True
            user.save()
            return super().validate(attrs)