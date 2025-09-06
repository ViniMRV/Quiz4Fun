
from django.db import models
from django.contrib.auth.models import AbstractUser


def user_profile_pic_path(instance, filename):
    ext = filename.split('.')[-1]
    email = instance.email.replace('@', '_at_').replace('.', '_')
    filename = f"{email}_profile_pic.{ext}"
    return f"profile_pics/{email}/{filename}"


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    activation_token = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

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