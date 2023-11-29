import pytest
from rest_framework.authtoken.models import Token


@pytest.fixture
def api_client():
	from rest_framework.test import APIClient
	return APIClient()

@pytest.fixture
def api_client_factory(api_client):
	def client(user):
		api_client.force_authenticate(user=user)
		return api_client
	return client

@pytest.fixture
def admin_client(api_client_factory, admin):
	return api_client_factory(admin)

@pytest.fixture
def user_client(api_client_factory, user):
	return api_client_factory(user)

@pytest.fixture
def user_client_2(api_client_factory, user_2):
	return api_client_factory(user_2)
