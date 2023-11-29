from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from src.core.serializers import MessageSerializer

from .serializers import (
	UserSerializer, LoginSerializer, 
	ForgotPasswordSerializer, ResetPasswordSerializer,
	AuthResponseSerializer,
)

User = get_user_model()

# Create your views here.
class AuthViewSet(viewsets.ViewSet):

	def get_response_payload(self, user):
		token = RefreshToken.for_user(user)
		return {
			'access_token': str(token.access_token),
			'refresh_token': str(token),
			'user': UserSerializer(user).data,
			'message': 'Login successful'
		}
	
	@extend_schema(
		request=LoginSerializer,
		responses={
			200: AuthResponseSerializer,
			400: MessageSerializer,
		}
	)
	@action(detail=False, methods=['POST'])
	def login(self, request):
		"""
		Login user
		"""
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		response_payload = self.get_response_payload(user)
		return Response(response_payload)
	
	@extend_schema(
		request=UserSerializer,
		responses={
			201: AuthResponseSerializer,
			400: MessageSerializer,
		}
	)
	@action(detail=False, methods=['POST'])
	def signup(self, request):
		"""
		Signup a new user
		"""
		serializer = UserSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		response_payload = self.get_response_payload(user)
		response_payload['message'] = 'Signup successful'
		return Response(response_payload, status=201)
	
	@extend_schema(
		request=ForgotPasswordSerializer,
		responses={
			200: MessageSerializer,
			400: MessageSerializer,
		}
	)
	@action(detail=False, methods=['POST'], url_path='forgot-password')
	def forgot_password(self, request):
		"""
		Initiate password reset process
		"""
		serializer = ForgotPasswordSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.save()
		return Response({"message": f"OTP sent to {email}, use the code to complete password reset"})
	
	@extend_schema(
		request=ResetPasswordSerializer,
		responses={
			200: MessageSerializer,
			400: MessageSerializer,
		}
	)
	@action(detail=False, methods=['POST'], url_path='reset-password')
	def reset_password(self, request):
		"""
		Complete password reset process
		"""
		serializer = ResetPasswordSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({"message": "Password changed successfully"})
