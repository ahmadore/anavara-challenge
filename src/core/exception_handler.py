import logging
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, AuthenticationFailed
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
	if isinstance(exc, ValidationError):
		if isinstance(exc.detail, dict):
			# If the error detail is a dictionary, convert it to {field: error_detail}
			error_data = {}
			message = list(exc.detail.values())[0]
			if isinstance(message, list):
				message = ' '.join(message)
			for field, errors in exc.detail.items():
				error_data[field] = list([str(error) for error in errors])
			return Response({'message': message, 'errors': error_data}, status=400)

	message = exc.detail if hasattr(exc, 'message') else str(exc)
	logging.warning({"Unhandled exception": message})
	if type(exc) in [NotAuthenticated, PermissionDenied, AuthenticationFailed, InvalidToken]:
		status = 401
	elif type(exc) in [ObjectDoesNotExist, Http404]:
		status = 404
	else:
		status = 400
	
	return Response({'message': message}, status=status)
