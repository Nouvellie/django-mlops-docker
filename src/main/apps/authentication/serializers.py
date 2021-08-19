from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


# class SignUpSerializer(serializers.ModelSerializer):
# 	password = serializers.CharField(max_length=68, min_length=8, write_only=True)

# 	class Meta:
# 		model = User
# 		fields = ['email', 'username', 'password']

# 		def validate(self, attrs):
# 			email = attrs.get('email', '')
# 			username = attrs.get('username', '')

# 			if not username.isalnum():
# 				raise serializers.ValidationError("The username should only contain alphanumeric characters.")
# 			return attrs
# 			# return super().validate(attrs)

# 		def create(self, validated_data):
# 			return User.objects.create_user(**validated_data)



class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'user_name', 'email')


class SignUpSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('id', 'user_name', 'email', 'password', 'password2')
		extra_kwargs = {'password': {'write_only': True}, 'password2': {'write_only': True},}

	def create(self, validated_data):
		print(validated_data)
		password = validated_data.pop('password', None)
		validated_data.pop('password2', None)
		print(password)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password": "Password fields didn't match."})

		return attrs

	def update(self, instance, validated_data):
		print("jaja!!!")
		for attr, value in validated_data.items():
			if attr == 'password':
				instance.set_password(value)
			else:
				setattr(instance, attr, value)
		instance.save()
		return instance

class SignInSerializer(serializers.ModelSerializer):
	user_name = serializers.CharField()
	password = serializers.CharField()

	def validate(self, data):
		user = authenticate(**data)
		if user and user.is_active:
			return user
		raise serializers.ValidationError("Incorrect credentials.")