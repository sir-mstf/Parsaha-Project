from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login-page'),
    path('registration/', views.RegisterView.as_view(), name='register-page'),
    path('registration/complete/<int:user_id>', views.CompleteProfileView.as_view(), name='register-complete-page'),
    path('activate-account/<email_active_code>', views.ActiveAccountView.as_view(), name='activate-account'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('compelete-profile/<int:pk>', views.EditProfileView.as_view(), name='edit-profile-view'),
    path('forget-password', views.ForgetPasswordView.as_view(), name='forget-password-page'),
    path('reset-password/<email_active_code>', views.ResetPasswordView.as_view(), name='reset-password-page'),
]