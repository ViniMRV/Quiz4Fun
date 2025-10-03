
from django.db import models
from django.contrib.auth.models import AbstractUser


def user_profile_pic_path(instance, filename):
    """
    Gera o caminho para salvar a foto de perfil do usuário.
    Recebe a instância do usuário e o nome do arquivo enviado, gera o caminho formatado para salvar a imagem.

    :param instance: Instância do usuário.
    :type instance: Users.User
    :param filename: Nome do arquivo enviado.
    :type filename: str
    :return: Caminho formatado para salvar a imagem.
    :rtype: str
    """
    ext = filename.split('.')[-1]
    email = instance.email.replace('@', '_at_').replace('.', '_')
    filename = f"{email}_profile_pic.{ext}"
    return f"profile_pics/{email}/{filename}"


class User(AbstractUser):
    """
    Modelo customizado de usuário.
    Adiciona campos para ativação por token, e-mail único e foto de perfil.
    Herda de AbstractUser do Django.
    """
    activation_token = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)

    def __str__(self):
        """
        Retorna o nome completo do usuário.

        :return: Nome completo do usuário.
        :rtype: str
        """
        return f"{self.first_name} {self.last_name}"
    
    
class UserQuizResult(models.Model):
    """
    Modelo que relaciona usuário, quiz e resultado obtido.
    Armazena o resultado do quiz para cada usuário, incluindo data de criação.
    """
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quizzes.Quiz', on_delete=models.CASCADE)
    result = models.ForeignKey('Quizzes.Result', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Retorna uma descrição do resultado do quiz para o usuário.

        :return: Texto descritivo do resultado do quiz para o usuário.
        :rtype: str
        """
        return f"Resultado de {self.user.first_name} {self.user.last_name} no Quiz {self.quiz}: {self.result.name}"