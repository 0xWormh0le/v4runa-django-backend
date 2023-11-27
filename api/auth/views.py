from django.contrib.auth.models import update_last_login
from rest_framework import status, parsers, renderers
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    UpdateAPIView
)
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import User
from .serializers import AuthTokenObtainPairSerializer
from ..user.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    PasswordUpdateSerializer
)


class LoginView(TokenObtainPairView):
    """
    User login view.
    """
    serializer_class = AuthTokenObtainPairSerializer


class RegisterView(CreateModelMixin, GenericAPIView):
    serializer_class = UserCreateSerializer
    authentication_classes = ()

    def post(self, request):
        """User registration view."""
        return self.create(request)


class ProfileView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(
            instance=request.user,
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PassworUpdatedView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordUpdateSerializer

    def get_object(self):
        return self.request.user


class EmailDuplicateView(RetrieveAPIView):
    """
    Check email duplication by param specified by `email`
    """

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        duplicate = User.objects.filter(email=email).first()
        return Response({
            'duplicate': duplicate is not None
        })
