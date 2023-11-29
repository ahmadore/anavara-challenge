import json
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_user_endpoint_authentication_required_fail(api_client, user):
	url = reverse('users-list')
	resp = api_client.get(url)
	assert resp.status_code == 401


@pytest.mark.django_db
def test_user_endpoint_authentication_required_pass(user_client, user):
	url = reverse('users-list')
	resp = user_client.get(url)
	assert resp.status_code == 200
	assert len(resp.json()['results']) == 1


@pytest.mark.django_db
def test_user_create_endpoint_permission_fail(api_client, user_data):
	url = reverse('users-list')
	resp = api_client.post(
		url, data=user_data
	)
	assert resp.status_code == 401


@pytest.mark.django_db
def test_user_create_endpoint_unique_email_check(user_client, user_data):
	url = reverse('users-list')
	resp = user_client.post(
		url, data=user_data
	)
	assert resp.status_code == 400
	assert b'user with this email already exists.' in resp.content


@pytest.mark.django_db
def test_user_create_endpoint_unique_email_check(user_client, user_data_2):
	url = reverse('users-list')
	resp = user_client.post(
		url, data=user_data_2
	)
	assert resp.status_code == 201
