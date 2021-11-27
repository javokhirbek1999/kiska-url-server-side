from django.urls import path

from user import views

from .views.url_views import OriginalUrlApiView

app_name = 'urls'

urlpatterns = [
    path('', OriginalUrlApiView.as_view(), name='orginal'),
]