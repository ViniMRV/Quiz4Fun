from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('menu/', views.quiz_menu, name='quiz_menu'),
    path('my/', views.user_quizzes, name='user_quizzes'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/setup/', views.quiz_setup, name='quiz_setup'),
    path('<int:quiz_id>/add-results/', views.add_results, name='add_results'),
    path('<int:quiz_id>/add-questions/', views.add_questions, name='add_questions'),
    path('<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
]
