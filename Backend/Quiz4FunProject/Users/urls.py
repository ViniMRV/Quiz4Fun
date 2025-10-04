from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register_user'),
    path('login/', views.LoginUserView.as_view(), name='login_user'),
    path('logout/', views.LogoutUserView.as_view(), name='logout_user'),
    path('activate/<str:token>/', views.ActivateUserView.as_view(), name='activate_user'),
    path(
        'activation-email-sent/',
        lambda request: render(request, 'users/activation_email_sent.html'),
        name='activation_email_sent'
    ),
    path("password_reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
