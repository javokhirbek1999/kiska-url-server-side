from django.http.response import HttpResponse
from django.shortcuts import redirect

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


from ..serializers import url_serializer
from ..models.url import OriginalURL


class OriginalUrlApiView(generics.ListCreateAPIView):
    """API view for creating and listing urls"""
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = url_serializer.OriginalUrlSerializer
    queryset = OriginalURL.objects.all()

class RedirectApiView(APIView):

    """API view for redirecting to original urls and updating visited count"""

    def get(self, request, *args, **kwargs):
        url_object = OriginalURL.objects.get(urlHash=kwargs.get('pk'))
        url_object.visited += 1
        url_object.save()
        return redirect(url_object.url)