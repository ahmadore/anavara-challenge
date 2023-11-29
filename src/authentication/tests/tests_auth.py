import re
import json
import pytest
from django.urls import reverse
from django.core import mail
from django.core.mail.backends.console import EmailBackend
from django.test import override_settings


def extract_otp_from_email(email_body):
	otp_pattern = r'(\b\d{6}\b)'  # Regular expression to match a 6-digit number
	match = re.search(otp_pattern, email_body)
	if match:
		return match.group()
	return None

@pytest.mark.django_db
def test_forgot_password_fails_user_does_not_exists(api_client, email):
	send_otp_url = reverse('auth-forgot-password')
	resp = api_client.post(
		send_otp_url, data={'email': email}
	)
	assert resp.status_code == 400
	assert b'User with the given email does not exist' in resp.content


@pytest.mark.django_db
def test_forgot_password_pass(api_client, user, email):
	send_otp_url = reverse('auth-forgot-password')
	resp = api_client.post(
		send_otp_url, data={'email': email}
	)
	assert resp.status_code == 200
	assert b'OTP sent to rob@example.com, use the code to complete password reset' in resp.content
	# check that email was sent out
	assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_reset_password_fails_wrong_code(api_client, user, email, default_password):
	send_otp_url = reverse('auth-forgot-password')
	resp = api_client.post(
		send_otp_url, data={'email': email}
	)
	assert resp.status_code == 200
	assert len(mail.outbox) == 1

	reset_password_url = reverse('auth-reset-password')
	wrong_code = '1234DD'
	payload = {
		'email': email,
		'otp_code': wrong_code,
		'password': default_password
	}
	resp_2 = api_client.post(
		reset_password_url, data=payload,
	)
	assert resp_2.status_code == 400
	assert b'Invalid or Expired OTP' in resp_2.content

@pytest.mark.django_db
def test_reset_password_pass(api_client, user, email, default_password):
	send_otp_url = reverse('auth-forgot-password')
	resp = api_client.post(
		send_otp_url, data={'email': email}
	)
	assert resp.status_code == 200

	assert len(mail.outbox) == 1
	
	sent_email = mail.outbox[0]
	email_body = sent_email.body
	otp_code = extract_otp_from_email(email_body)

	reset_password_url = reverse('auth-reset-password')
	payload = {
		'email': email,
		'otp_code': otp_code,
		'password': default_password
	}
	resp_2 = api_client.post(
		reset_password_url, data=payload,
	)
	assert resp_2.status_code == 200
	assert b'Password changed successfully' in resp_2.content


@pytest.mark.django_db
@pytest.mark.parametrize("email, password", [
	('', ''), 
	('test@example.com', ''),
	('', 'nowyouseeme'),
	('test@example.com', 'nowyouseeme'),
	('test@example', 'nowyouseeme')
])
def test_login_fail_wrong_credential(email, password, api_client, user):
	login_url = reverse('auth-login')
	payload = {'email': email, 'password': password}
	resp = api_client.post(login_url, data=payload)
	assert resp.status_code == 400


@pytest.mark.django_db
def test_login_fail_user_does_not_exist(api_client, email, default_password):
	login_url = reverse('auth-login')
	payload = {'email': email, 'password': default_password}
	resp = api_client.post(login_url, data=payload)
	assert resp.status_code == 400
	assert resp.json()['message'] == 'User with the given email does not exist'


@pytest.mark.django_db
def test_login_pass(api_client, email, default_password, user):
	login_url = reverse('auth-login')
	payload = {'email': email, 'password': default_password}
	resp = api_client.post(login_url, data=payload)
	assert resp.status_code == 200
	assert 'access_token' in resp.json()


@pytest.mark.django_db
def test_signup_fail_invalid_data(api_client, user_data, invalid_email):
	signup_url = reverse('auth-signup')
	user_data['email'] = invalid_email
	resp = api_client.post(signup_url, data=user_data)
	assert resp.status_code == 400
	assert b'Enter a valid email address.' in resp.content


@pytest.mark.django_db
def test_signup_fail_duplicate_data(api_client, user_data, user):
	signup_url = reverse('auth-signup')
	resp = api_client.post(signup_url, data=user_data)
	assert resp.status_code == 400
	assert b'user with this email already exists.' in resp.content


@pytest.mark.django_db
def test_signup_pass(api_client, user_data):
	signup_url = reverse('auth-signup')
	resp = api_client.post(signup_url, data=user_data)
	assert resp.status_code == 201
