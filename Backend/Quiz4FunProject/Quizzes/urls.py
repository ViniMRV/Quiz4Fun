from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.QuizListView.as_view(), name='quiz_list'),
    path('menu/', views.QuizMenuView.as_view(), name='quiz_menu'),
    path('my/', views.UserQuizzesView.as_view(), name='user_quizzes'),
    path('create/', views.CreateQuizView.as_view(), name='create_quiz'),
    path('<int:quiz_id>/setup/', views.QuizSetupView.as_view(), name='quiz_setup'),
    path('<int:quiz_id>/add-results/', views.AddResultsView.as_view(), name='add_results'),
    path('<int:quiz_id>/add-questions/', views.AddQuestionsView.as_view(), name='add_questions'),
    path('<int:quiz_id>/take/', views.TakeQuizView.as_view(), name='take_quiz'),
    path('<int:quiz_id>/result/', views.QuizResultView.as_view(), name='quiz_result'),
]
