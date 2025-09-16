from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/setup/', views.quiz_setup, name='quiz_setup'),
    path('<int:quiz_id>/add-results/', views.add_results, name='add_results'),
    path('<int:quiz_id>/add-questions/', views.add_questions, name='add_questions'),
    #path('meus-quizzes/', views.user_quizzes, name='user_quizzes'),
]
