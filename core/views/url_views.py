from django.http.response import HttpResponse
from django.shortcuts import redirect

from rest_framework import generics, permissions
from rest_framework.views import APIView


from ..serializers import url_serializer
from ..models.url import OriginalURL, ShortURL

class OriginalUrlApiView(generics.ListCreateAPIView):
    """API view for creating and listing original url"""
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = url_serializer.OriginalUrlSerializer
    queryset = OriginalURL.objects.all()


class ShortUrlApiView(generics.ListAPIView):
    """API view for creating and listing shortened url"""
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = url_serializer.ShortenedUrlSerializer
    queryset = ShortURL.objects.all()



class RedirectApiView(APIView):

    """API view for redirecting to original urls and updating visited count"""

    def get(self, request, *args, **kwargs):
        short_url_object = ShortURL.objects.get(urlHash=kwargs.get('pk'))
        short_url_object.visited += 1
        short_url_object.save()
        return redirect(short_url_object.originalURL.url)