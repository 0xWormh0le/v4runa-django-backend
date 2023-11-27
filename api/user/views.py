from user.models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsAdminOrGeneralManager


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    authentication_classes = [IsAuthenticated]
    permission_classes = [IsAdminOrGeneralManager]

    def get_serializer_class(self):
        if not self.request:
            return UserSerializer
        if self.request.method in ['POST']:
            return UserCreateSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        else:
            # Default for get and other requests is the read only serializer
            return UserSerializer
