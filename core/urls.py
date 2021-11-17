from django.urls import path

from user import views

from .views.url_views import OriginalUrlApiView, ShortUrlApiView

app_name = 'urls'

urlpatterns = [
    path('org/', OriginalUrlApiView.as_view(), name='orginal'),
    path('short/', ShortUrlApiView.as_view(), name='short'),
]