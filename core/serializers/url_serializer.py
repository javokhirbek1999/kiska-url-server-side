from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework import serializers

from ..models import url
from ..utils.urls import utils

class OriginalUrlSerializer(serializers.ModelSerializer):

    """Serializer for Original URL API View"""

    class Meta:
        model = url.OriginalURL
        fields = ('id','user', 'get_user_username', 'url', 'shortened', 'visited', 'date_created', 'shortURL', 'urlHash')

        extra_kwargs = {
            "user": {"read_only": True},
            "urlHash": {"read_only": True},
            "shortURL": {"read_only": True},
            "visited": {"read_only": True},
        }

    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user
        return attrs
    
    def create(self, validated_data):

        instnace = None
        try:
            instance = self.Meta.model.objects.get(**validated_data)
            instance.shortened += 1
            instance.save()
        except ObjectDoesNotExist:
            instance = self.Meta.model.objects.create(**validated_data)
            hashedURL = utils.hash_the_url(instance.user, instance.url)
            instance.shortURL = f'{settings.DEFAULT_DOMAIN}{hashedURL}/'
            instance.urlHash = hashedURL
            instance.save() 
        
        return instance
