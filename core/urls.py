from django.urls import path

from user import views

from .views.url_views import OriginalUrlApiView, ShortUrlApiView, AllOriginalUrlApiView, AllShortUrlApiView

app_name = 'urls'

urlpatterns = [
    path('org/', OriginalUrlApiView.as_view(), name='orginal'),
    path('short/', ShortUrlApiView.as_view(), name='short'),
    path('all-org/', AllOriginalUrlApiView.as_view(), name='all-org'),
    path('all-short/', AllShortUrlApiView.as_view(), name='all-short')
]