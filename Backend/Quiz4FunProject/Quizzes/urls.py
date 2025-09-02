from django.urls import path
from . import views

urlpatterns = [
    path('meus-quizzes/', views.user_quizzes, name='user_quizzes'),
]
