from rest_framework.views import APIView
from rest_framework import permissions, generics

from . import serializers


class UserAPIView(generics.CreateAPIView):
    """API view for User Model"""
    # permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer
