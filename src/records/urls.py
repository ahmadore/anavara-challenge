from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

medical_record_router = DefaultRouter()

medical_record_router.register('medical-records', views.MedicalRecordViewSet, basename='medical-records')


urlpatterns = [
	path('', include(medical_record_router.urls)),
]
