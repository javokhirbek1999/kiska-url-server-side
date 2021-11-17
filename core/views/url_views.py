from django.http.response import HttpResponse
from django.shortcuts import redirect

from rest_framework import generics, permissions
from rest_framework.views import APIView


from ..serializers import url_serializer
from ..models.url import AllOriginalURL, OriginalURL, ShortURL, AllShortURL

class OriginalUrlApiView(generics.ListCreateAPIView):
    """API view for creating and listing original url"""
    
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = url_serializer.OriginalUrlSerializer
    queryset = OriginalURL.objects.all()


class ShortUrlApiView(generics.ListAPIView):
    """API view for creating and listing shortened url"""
    
    permission_classes = (permissions.AllowAny,)
    serializer_class = url_serializer.ShortenedUrlSerializer
    queryset = ShortURL.objects.all()



class RedirectApiView(APIView):

    """API view for redirecting to original urls and updating visited count"""

    def get(self, request, *args, **kwargs):
        short_url_object = ShortURL.objects.get(urlHash=kwargs.get('pk'))
        all_short_url_instance = AllShortURL.objects.get(url=short_url_object)
        all_short_url_instance.visited += 1
        short_url_object.visited += 1
        all_short_url_instance.save()
        short_url_object.save()
        return redirect(short_url_object.originalURL.url)


class AllOriginalUrlApiView(generics.ListAPIView):
    """API view for listing all Original URLs created so far"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = url_serializer.AllOriginalUrlSerializer
    queryset = AllOriginalURL.objects.all()


class AllShortUrlApiView(generics.ListAPIView):
    """API view for listing all Shortened URLs created so far"""
    
    permission_classes = (permissions.AllowAny,)
    serializer_class = url_serializer.AllShortUrlSerializer
    queryset = AllShortURL.objects.all()