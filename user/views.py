from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate

from rest_framework import permissions, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from . import serializers
from .permissions import IsOwnerOrReadOnly, IsOwner
from .utils import Utils 


class UserAPIView(generics.CreateAPIView):
    """API view for User Model"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer


class UserPasswordChange(generics.UpdateAPIView):
    """API view for changing user password"""
    serializer_class = serializers.ChangePasswordSerializer
    model = get_user_model()
    permission_classes = (IsOwner,)

    def get_object(self): 
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.user = self.get_object()
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
    permission_classes = (IsOwner,)
    serializer_class = serializers.RequestResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = get_user_model().objects.get(email=serializer.data.get('email'))
            token = Token.objects.get_or_create(user=user)[0].key
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('user:password-reset-confirm')
            absurl = 'http://'+current_site+relativeLink
            email_body = f'Hello!\nUse the token below to reset your password by following the link below to reset your password\nTOKEN: {token}\nLINK:{absurl}'
            data = {"email_subject":"Password Reset", "email_body":email_body, "to_email":user.email}

            Utils.send_mail(data)

            return Response({
                'status': "success",
                'message': "We have sent you password reset link to your email",
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        

class ConfirmResetPasswordAPIView(generics.CreateAPIView):
    """Password reset confirmation API View"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ConfirmResetPasswordSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            rel = reverse('user:password-reset')
            return redirect(rel)

        return Response({
            'status': 'failed',
            'message': 'Invalid credentials',
            'code': status.HTTP_400_BAD_REQUEST
             }, status=status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordAPIView(generics.UpdateAPIView):

    """Password rest API View"""

    permission_classes = (IsOwner,)
    serializer_class = serializers.ResetPasswordSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        self.user = self.get_object()
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


