from rest_framework import serializers
from .models import User


class UserInfoSerializer(serializers.ModelSerializer):
	is_staff = serializers.BooleanField()

	class Meta:
		model = User
		fields = '__all__'
		read_only_fields = (
			'id',
			'last_login', 
			'is_superuser', 
			'is_active',
			'date_joined', 
			'groups', 
			'user_permissions',
			'created',
			'updated',
		)
		extra_kwargs = {
			'password': {'write_only': True}
		}
	
	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		return user
