from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _

from src.core.models import BaseModel

# Create your models here.
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
	USERNAME_FIELD = 'email'

	email = models.EmailField(_('email'), unique=True, max_length=255)
	first_name = models.CharField(_("first name"), max_length=150)
	last_name = models.CharField(_("last name"), max_length=150)
	is_staff = models.BooleanField(_('staff status'), default=False)
	is_active = models.BooleanField(_('active'), default=True)

	class Meta:
		db_table = 'users'
		verbose_name = _('user')
		verbose_name_plural = _('users')
	

	def get_full_name(self):
		full_name = "%s %s" % (self.first_name, self.last_name)
		return full_name.strip()
	
	def __str__(self):
		return self.get_full_name()
	
