from rest_framework import serializers

from ..models import url


class OriginalUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = url.OriginalURL
        fields = ('id','user', 'get_user_username', 'url', 'date_created')


class ShortenedUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = url.ShortURL
        fields = ('id', 'get_username', 'get_original_url', 'short_url', 'date_created')


class AllOriginalUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = url.AllOriginalURL
        fields = ('id', 'url', 'shortened', 'date_created')


class AllShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = url.AllShortURL
        fields = ('id', 'url', 'visited', 'date_created')