from django.contrib.auth import get_user_model, authenticate
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = get_user_model()
        fields = ('id','email','user_name','password','is_active','get_date_joined','get_date_updated')
        extra_kwargs = {
            'password': {'style':{'input_type':'password'}, 'write_only':True, 'min_length':5}
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class CreateSuperuserSerializer(serializers.ModelSerializer):
    """Serializer for creating Admin User"""
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'user_name', 'password', 'get_date_joined', 'get_date_updated')
        extra_kwargs = {
            'password': {'style':{'input_type':'password'}, 'write_only':True, 'min_length':5}
        }
    
    def create(self, validated_data):
        return get_user_model().objects.create_superuser(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""

    model = get_user_model()

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RequestResetPasswordSerializer(serializers.Serializer):
    """Serializer for password reset request"""

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        
        if not get_user_model().objects.filter(email=attrs.get('email')).exists():
            msg = _('User linked to given email does not exist')
            raise serializers.ValidationError(msg)
        
        return attrs


class ConfirmResetPasswordSerializer(serializers.Serializer):
    """Serializer for password reset confirmation"""

    token = serializers.CharField(max_length=1000)

    def validate(self, attrs):
        token = attrs.get('token')

        # import pdb
        # pdb.set_trace()
        if not Token.objects.get(key=token):
            raise serializers.ValidationError(_('Token is invalid, please request new one'))

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for password reset"""

    new_password = serializers.CharField(max_length=250)
    confirm_password = serializers.CharField(max_length=250)

    def validate(self, attrs):
        password1 = attrs.get('new_password')
        password2 = attrs.get('confirm_password')

        if password1 != password2:
            raise serializers.ValidationError(_('Password did not match, make sure passwords does match'))

        return attrs


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for creating authentication token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Validation Error, invalid credentails')
            raise serializers.ValidationError(msg, code='authentication')
        
        if not user.is_active:
            msg = _('User is blocked, please contact admin')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user

        return attrs
