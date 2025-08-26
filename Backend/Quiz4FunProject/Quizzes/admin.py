from django.contrib import admin

from django.contrib import admin
from .models import Quiz, Question, Result, Option, OptionScore

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Option)
admin.site.register(OptionScore)
