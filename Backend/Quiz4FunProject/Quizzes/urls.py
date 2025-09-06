from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add-questions/', views.add_questions, name='add_questions'),  # placeholder
]
