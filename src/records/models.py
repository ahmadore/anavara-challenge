from django.db import models
from src.core.models import BaseModel

# Create your models here.
class MedicalRecord(BaseModel):
	user_id = models.CharField(max_length=100)
	patient_name = models.CharField(max_length=255)
	date_of_birth = models.DateField()
	diagnosis = models.TextField(blank=True, null=True)
	treatment = models.TextField(blank=True, null=True)
	date_of_treatment = models.DateField()
	doctor = models.CharField(max_length=255)

	def __str__(self):
		return f'{self.patient_name} - {self.date_of_treatment}'
