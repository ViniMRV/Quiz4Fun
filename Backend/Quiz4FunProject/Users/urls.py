from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('status/', views.user_status, name='user_status'),
    path('activate/<str:token>/', views.activate_user, name='activate_user'),
    path('activation-email-sent/', lambda request: render(request, 'users/activation_email_sent.html'), name='activation_email_sent'),
]
