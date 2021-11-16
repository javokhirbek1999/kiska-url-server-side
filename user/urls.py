from django.urls import path

from . import views


app_name = 'user'


urlpatterns = [
    path('create/', views.UserAPIView.as_view(), name='create'),
    path('all/', views.AllUsers.as_view(), name='all'),
    path('all/<str:pk>/', views.SingleUser.as_view(), name='single'),
    path('token/', views.AuthTokenAPIView.as_view(), name='token')
]