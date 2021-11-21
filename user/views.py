from django.contrib.auth import get_user_model

from rest_framework import permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from . import serializers

from .permissions import IsOwnerOrReadOnly


class UserAPIView(generics.CreateAPIView):
    """API view for User Model"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer


class AllUsers(generics.ListAPIView):
    """API view for listing all users"""
    permission_classes = (permissions.AllowAny,)
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
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = serializers.AuthTokenSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.user_name,
            'email': user.email
        })


