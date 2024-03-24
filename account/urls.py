
from django.contrib import admin
from django.urls import path
from account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.UserRegistration.as_view(), name='register' ),
    path('login/', views.UserLogin.as_view(), name='login' ),
    path('profile/', views.UserProfile.as_view(), name='profile' ),
    path('password-change/', views.UserChangePasswordView.as_view(), name='password-change' ),
    path('send-email/', views.UserEmailSendView.as_view(), name='send-email'),
    path('password-reset/<uid>/<token>/', views.UserResetPasswordView.as_view(), name='reset-password'),
]
