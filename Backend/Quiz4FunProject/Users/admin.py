from django.contrib import admin

from django.contrib import admin
from .models import User, UserQuiz, UserQuizResult

admin.site.register(User)
admin.site.register(UserQuiz)
admin.site.register(UserQuizResult)
