from datetime import datetime
from django.db import models
from django.contrib.auth.hashers import check_password as django_check_password


def user_profile_pic_path(instance, filename):
    ext = filename.split('.')[-1]
    email = instance.email.replace('@', '_at_').replace('.', '_')
    filename = f"{email}_profile_pic.{ext}"
    return f"profile_pics/{email}/{filename}"

class User(models.Model):
    last_login = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=64, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True
    

class UserQuiz(models.Model):
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quizzes.Quiz', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quiz}: Criado por {self.user.first_name} {self.user.last_name}"
    
class UserQuizResult(models.Model):
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quizzes.Quiz', on_delete=models.CASCADE)
    result = models.ForeignKey('Quizzes.Result', on_delete=models.CASCADE)

    def __str__(self):
        return f"Resultado de {self.user.first_name} {self.user.last_name} no Quiz {self.quiz}: {self.result.name}"