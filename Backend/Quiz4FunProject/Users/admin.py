from django.contrib import admin
from .models import User, UserQuiz, UserQuizResult

class UserAdmin(admin.ModelAdmin):
	exclude = ('password',)
	list_display = ('first_name', 'last_name', 'email', 'is_active')

admin.site.register(User, UserAdmin)
admin.site.register(UserQuiz)
admin.site.register(UserQuizResult)
