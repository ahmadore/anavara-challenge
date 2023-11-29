from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from .models import OTP

User = get_user_model()


class ValidateEmailMixin(serializers.Serializer):
	def validate_email(self, email):
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			raise serializers.ValidationError("User with the given email does not exist")
		return email


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id',
			'first_name',
			'last_name', 
			'email',
			'password',
		)
		extra_kwargs = {
			'id': {'read_only': True},
			'password': {'write_only': True}
		}


class AuthResponseSerializer(serializers.Serializer):
	access_token = serializers.CharField()
	refresh_token = serializers.CharField()
	user = UserSerializer()
	message = serializers.CharField()


class LoginSerializer(ValidateEmailMixin):
	email = serializers.EmailField()
	password = serializers.CharField()

	def validate(self, data):
		data = super().validate(data)
		email = data['email']
		password = data['password']
		user = User.objects.get(email=email)
		if not user.check_password(password):
			raise serializers.ValidationError("Invalid Email or Password")
		return data

	def save(self):
		email = self.validated_data.get('email')
		return User.objects.get(email=email)


class ForgotPasswordSerializer(ValidateEmailMixin):
	email = serializers.EmailField()
	
	def save(self):
		data = self.validated_data
		email = data.get('email')

		otp_instance = OTP.generate_otp(email)
		# Send email OTP token for password reset
		send_mail(
			'Password Reset Request',
			f'Use the code to reset password: {otp_instance.code}',
			'from@example.com',
			[email],
			fail_silently=False,
		)
		return email


class ResetPasswordSerializer(ValidateEmailMixin):
	email = serializers.EmailField()
	otp_code = serializers.CharField()
	password = serializers.CharField()

	def validate(self, data):
		email = data['email']
		otp_code = data['otp_code']
		otp_instance = OTP.objects.filter(
			email=email, code=otp_code, used=False
		).order_by('-created_at').first()

		if not otp_instance:
			raise serializers.ValidationError("Invalid or Expired OTP")
		
		otp_validity_duration = timezone.now() - otp_instance.created_at
		if otp_validity_duration.total_seconds() > 300: # 5mins, can be adjusted as needed
			raise serializers.ValidationError("OTP expired")
		otp_instance.used = True
		otp_instance.save()
		return super().validate(data)
		
	def save(self):
		data = self.validated_data
		email = data['email']
		new_password = data['password']
		user = User.objects.get(email=email)
		user.set_password(new_password)
		user.save()
		return user
