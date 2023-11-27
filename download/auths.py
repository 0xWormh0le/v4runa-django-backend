from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class DownloadAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.query_params.get('auth')
        
        if not auth:
            return None

        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(auth)
            user = jwt_auth.get_user(validated_token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Authentication failed')

        return (user, None)
