from django.db import models


def user_profile_pic_path(instance, filename):
    nome_usuario = f"{instance.first_name}{instance.last_name}".replace(" ", "")
    ext = filename.split('.')[-1]
    filename = f"{nome_usuario.lower()}_profile_pic.{ext}"
    return f"profile_pics/{nome_usuario}/{filename}"

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)

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