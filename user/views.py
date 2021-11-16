from django.contrib.auth import get_user_model

from rest_framework import permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from . import serializers

from .permissions import IsOwnerOrReadOnly


class UserAPIView(generics.CreateAPIView):
    """API view for User Model"""
    serializer_class = serializers.UserSerializer


class AllUsers(generics.ListAPIView):
    """API view for listing all users"""
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()


class SingleUser(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving a specific user by username"""
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = serializers.UserSerializer
    
    def get_object(self, **kwargs):
        return get_user_model().objects.get(user_name=self.kwargs.get('pk'))


class AuthTokenAPIView(ObtainAuthToken):
    """API view for obtaining authentication token"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


