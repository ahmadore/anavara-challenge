from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import MedicalRecordSerializer
from .models import MedicalRecord

# Create your views here.
class MedicalRecordViewSet(viewsets.ModelViewSet):
	# permission_classes = [IsAuthenticated]
	serializer_class = MedicalRecordSerializer

	def get_queryset(self):
		if not self.request.user.is_staff:
			return MedicalRecord.objects.filter(user_id=self.request.user.id)
		return MedicalRecord.objects.all()
