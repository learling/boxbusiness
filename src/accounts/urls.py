from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),  
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.users, name='users'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="accounts/password/reset.html"),
        name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password/reset_sent.html"), 
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password/reset_form.html"), 
        name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password/reset_done.html"), 
        name="password_reset_complete")
]
