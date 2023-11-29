import json
import pytest
from django.urls import reverse


@pytest.mark.django_db
def tests_create_medical_record_fails_user_does_not_exist(user_client, medical_record_data_invalid):
	url = reverse('medical-records-list')
	resp = user_client.post(url, data=medical_record_data_invalid)
	assert resp.status_code == 400
	assert resp.json()['message'] == 'User with the given ID does not exist'


@pytest.mark.django_db
def tests_create_medical_record_fails_invalid_date(user_client, medical_record_data_invalid_date):
	url = reverse('medical-records-list')
	resp = user_client.post(url, data=medical_record_data_invalid_date)
	assert resp.status_code == 400
	assert resp.json()['message'] == 'Ensure treatment dates are in the future'


@pytest.mark.django_db
def tests_create_medical_record_pass(user_client, medical_record_data):
	url = reverse('medical-records-list')
	resp = user_client.post(url, data=medical_record_data)
	assert resp.status_code == 201


@pytest.mark.django_db
@pytest.mark.parametrize("client, result_count", [
	('user_client', 1), ('user_client_2', 0), ('admin_client', 1)
])
def tests_user_can_only_see_their_records(client, result_count, madical_record, request):
	url = reverse('medical-records-list')
	client = request.getfixturevalue(client)
	resp = client.get(url)
	assert resp.status_code == 200
	assert len(resp.json()['results']) == result_count
