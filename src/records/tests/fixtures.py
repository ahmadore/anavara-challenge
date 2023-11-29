import pytest
import uuid
from datetime import datetime, timedelta

from src.records.models import MedicalRecord

current_date = datetime.now().date()
interval = 30

past_date = current_date - timedelta(days=interval)
future_date = current_date + timedelta(days=interval)
date_format = "%Y-%m-%d"


@pytest.fixture
def medical_record_data_invalid():
	return {
		'user_id': str(uuid.uuid4()),
		'patient_name': 'Invalid User',
		'date_of_birth': past_date.strftime(date_format),
		'diagnosis': 'diagnosis abc',
		'treatment': 'treatment xyz',
		'date_of_treatment': future_date.strftime(date_format),
		'doctor': 'Doc Octavia'
	}


@pytest.fixture
def medical_record_data_invalid_date(user):
	return {
		'user_id': str(user.id),
		'patient_name': user.get_full_name(),
		'date_of_birth': past_date.strftime(date_format),
		'diagnosis': 'diagnosis abc',
		'treatment': 'treatment xyz',
		'date_of_treatment': current_date.strftime(date_format),
		'doctor': 'Doc Octavia'
	}


@pytest.fixture
def medical_record_data(user):
	return {
		'user_id': str(user.id),
		'patient_name': user.get_full_name(),
		'date_of_birth': past_date.strftime(date_format),
		'diagnosis': 'diagnosis abc',
		'treatment': 'treatment xyz',
		'date_of_treatment': future_date.strftime(date_format),
		'doctor': 'Doc Octavia'
	}

@pytest.fixture
def madical_record(medical_record_data):
	return MedicalRecord.objects.create(**medical_record_data)

