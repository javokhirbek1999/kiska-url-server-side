from django.urls import path

from . import views


app_name = 'user'


urlpatterns = [
    path('create/', views.UserAPIView.as_view(), name='create'),
    path('token/', views.AuthTokenAPIView.as_view(), name='token')
]