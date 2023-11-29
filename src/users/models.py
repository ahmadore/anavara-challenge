from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from src.core.models import BaseModel

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
	username = None

	email = models.EmailField(_('email'), unique=True, max_length=255)
	first_name = models.CharField(_("first name"), max_length=150)
	last_name = models.CharField(_("last name"), max_length=150)
	is_staff = models.BooleanField(_('staff status'), default=False)
	is_active = models.BooleanField(_('active'), default=True)

	objects = UserManager()

	class Meta:
		db_table = 'users'
		verbose_name = _('user')
		verbose_name_plural = _('users')
	

	def get_full_name(self):
		full_name = "%s %s" % (self.first_name, self.last_name)
		return full_name.strip()
	
	def __str__(self):
		return self.get_full_name()
	
