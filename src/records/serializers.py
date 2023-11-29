from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import MedicalRecord

User = get_user_model()


class MedicalRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = MedicalRecord
		fields = '__all__'
		read_only_fields = (
			'id', 
			'created', 
			'updated',
		)
	
	def validate_user_id(self, user_id):
		"""This method should call users service that checks if user exists"""
		try:
			user = User.objects.get(id=user_id)
		except User.DoesNotExist:
			raise serializers.ValidationError("User with the given ID does not exist")
		return user_id
	
	def validate_date_of_treatment(self, date_of_treatment):
		if date_of_treatment <= timezone.now().date():
			raise serializers.ValidationError("Ensure treatment dates are in the future")
		return date_of_treatment
