from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from src.core.serializers import MessageSerializer

from .models import User
from .serializers import UserInfoSerializer
# Create your views here.
class UserViewSet(
	viewsets.GenericViewSet, 
	mixins.CreateModelMixin, 
	mixins.ListModelMixin, 
	mixins.RetrieveModelMixin
	):
	serializer_class = UserInfoSerializer
	queryset = User.objects.all()
