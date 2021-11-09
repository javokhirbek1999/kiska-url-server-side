
from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','user_name','password','date_joined','is_active')
        extra_kwargs = {
            'password': {'style':{'input_type':'password'}, 'write_only':True, 'min_length':5}
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)