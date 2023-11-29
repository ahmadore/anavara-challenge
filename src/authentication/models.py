from django.db import models
import secrets

# Create your models here.
class OTP(models.Model):
	email = models.EmailField()
	code = models.CharField(max_length=6)
	created_at = models.DateTimeField(auto_now_add=True)
	used = models.BooleanField(default=False)

	@classmethod
	def generate_otp(cls, email):
		otp = secrets.randbelow(1000000)
		str_otp = f"{otp:06}"
		return cls.objects.create(email=email, code=str_otp)

