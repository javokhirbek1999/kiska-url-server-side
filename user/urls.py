from django.urls import path

from . import views


app_name = 'user'


urlpatterns = [
    path('create/', views.UserAPIView.as_view(), name='create'),
    path('create-superuser/', views.CreateSuperuserAPIView.as_view(), name='create-superuser'),
    path('change-password/<str:username>/', views.UserPasswordChange.as_view(), name='change-password'),
    path('password-reset-request/', views.RequestResetPasswordAPIView.as_view(), name='password-reset-request'),
    path('password-reset-confirmation/', views.ConfirmResetPasswordAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset/', views.ResetPasswordAPIView.as_view(), name='password-reset'),
    path('all/', views.AllUsers.as_view(), name='all'),
    path('all/profile/<str:pk>', views.SingleUser.as_view(), name='single-user'),
    path('token/', views.AuthTokenAPIView.as_view(), name='token')
]