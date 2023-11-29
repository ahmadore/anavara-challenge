from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

auth_router = DefaultRouter()
auth_router.register('auth', views.AuthViewSet, basename='auth')

urlpatterns = [
	path('', include(auth_router.urls)),
]
