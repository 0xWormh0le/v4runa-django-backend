from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..user.serializers import UserSerializer


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        return {
            'profile': UserSerializer(self.user).data,
            'token': data['access']
        }
