from rest_framework.views import APIView
from rest_framework import permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from . import serializers


class UserAPIView(generics.CreateAPIView):
    """API view for User Model"""
    serializer_class = serializers.UserSerializer


class AuthTokenAPIView(ObtainAuthToken):
    """API view for obtaining authentication token"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
