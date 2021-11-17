from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from ..models import url


class OriginalUrlSerializer(serializers.ModelSerializer):

    """Serializer for Original URL API View"""

    class Meta:
        model = url.OriginalURL
        fields = ('id','user', 'get_user_username', 'url', 'shortened', 'date_created')
    
    def create(self, validated_data):

        instnace = None
        try:
            instance = self.Meta.model.objects.get(**validated_data)
            instance.shortened += 1
            instance.save()
        except ObjectDoesNotExist:
            instance = self.Meta.model.objects.create(**validated_data)
        
        return instance


class ShortenedUrlSerializer(serializers.ModelSerializer):

    """Serializer for Short URL API View"""

    class Meta:
        model = url.ShortURL
        fields = ('id', 'get_username', 'get_original_url', 'shortURL', 'visited', 'date_created')
