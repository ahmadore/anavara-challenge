import pytest

@pytest.fixture
def email():
	return 'rob@example.com'

@pytest.fixture
def admin_email():
	return 'lady_ada@example.com'

@pytest.fixture
def default_password():
	return 'P@55W0rd'

@pytest.fixture
def user_data(default_password, email):
	return {
		'first_name': 'Robert',
		'last_name': 'Martin',
		'email': email,
		'password': default_password,
	}

@pytest.fixture
def user_data_2(default_password, admin_email):
	return {
		'first_name': 'Ada',
		'last_name': 'Augusta',
		'email': admin_email,
		'is_staff': True,
		'password': default_password,
	}

@pytest.fixture
def user_factory(db, django_user_model, default_password):
	def create_user(**kwargs):
		user = django_user_model.objects.create(**kwargs)
		user.set_password(default_password)
		user.save()
		return user
	return create_user


@pytest.fixture
def admin(user_factory, user_data_2):
	return user_factory(**user_data_2)


@pytest.fixture
def user(user_factory, user_data):
	return user_factory(**user_data)

@pytest.fixture
def user_2(user_factory, default_password):
	data = {
		'first_name': 'second',
		'last_name': 'Martin',
		'email': 'secondUser@test.com',
		'password': default_password,
	}
	return user_factory(**data)
