from django.contrib.auth import get_user_model
from django.http import request
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate

from rest_framework import permissions, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from . import serializers
from .permissions import IsOwnerOrReadOnly, IsOwner, AllowAny
from .utils import Utils 


class UserAPIView(generics.CreateAPIView):
    """API view for User Model"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer


class CreateSuperuserAPIView(generics.CreateAPIView):
    """API View for Creating Superuser (Admin User)"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.CreateSuperuserSerializer


class UserPasswordChange(generics.UpdateAPIView):
    """API view for changing user password"""
    serializer_class = serializers.ChangePasswordSerializer
    model = get_user_model()
    permission_classes = (IsOwner,)

    # If user does not exist, returns None
    def get_object(self, **kwargs): 
        User = get_user_model()
        user = None
        try:
            user = User.objects.get(user_name=self.kwargs.get('username'))
        except User.DoesNotExist:
            pass
        return user

    
    def update(self, request, *args, **kwargs):
        self.user = self.get_object();

        # If user does not exist, returns 404 NOT FOUND ERROR
        if self.user is None:
            return Response({
                'status': 'failed',
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'User does not exist'
            },status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password matches
            if not self.user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            
            self.user.set_password(serializer.data.get('new_password'))
            self.user.save()

            return Response({
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestResetPasswordAPIView(generics.CreateAPIView):
    """Request password reset API View"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RequestResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # If data is valid, then sedn confirmation email with url to reset password
        if serializer.is_valid():
            user = get_user_model().objects.get(email=serializer.data.get('email'))
            token = Token.objects.get_or_create(user=user)[0].key
            absurl = redirect('https://kiska-url.herokuapp.com/reset-password/'+token)
            email_body = f'Hello!\nUse the token below to reset your password by following the link below to reset your password\nTOKEN: {token}\nLINK:{absurl.url}'
            data = {"email_subject":"Password Reset", "email_body":email_body, "to_email":user.email}

            Utils.send_mail(data)

            return Response({
                'status': "success",
                'message': "We have sent you password reset link to your email",
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        

class ResetPasswordAPIView(generics.UpdateAPIView):

    """Password rest API View"""

    permission_classes = (IsOwner,)
    serializer_class = serializers.ResetPasswordSerializer

    def get_object(self, **kwargs): 
        user = None
        try:
            user = Token.objects.get(key=self.kwargs.get('token')).user
        except get_user_model().DoesNotExist:
            pass
        return user
    
    def update(self, request, *args, **kwargs):
        self.user = self.get_object()

        # If user does not exist, returns 404 NOT FOUND ERROR
        if self.user is None:
            return Response({
                'status': 'failed',
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'User does not exist'
            },status=status.HTTP_404_NOT_FOUND)


        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.user.set_password(serializer.validated_data.get('new_password'))
            self.user.save()

            return Response({
                'status': 'suceess',
                'message': 'Password reset successfully',
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'failed',
            'message': 'Passwords did not match',
            'code': status.HTTP_400_BAD_REQUEST,
        }, status=status.HTTP_400_BAD_REQUEST);


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
        print(self.kwargs.get('pk'))
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


