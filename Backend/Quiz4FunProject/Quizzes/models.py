from django.db import models

class Quiz(models.Model):
    """
    Modelo que representa um quiz.
    Armazena título, descrição, autor, data de criação e imagem principal.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name="quizzes")
    quiz_main_picture = models.ImageField(upload_to='quiz/main_images/', blank=True, null=True)

    def __str__(self):
        """
        Retorna o título do quiz.

        :return: Título do quiz.
        :rtype: str
        """
        return self.title

class Question(models.Model):
    """
    Modelo que representa uma questão de um quiz.
    Armazena o texto da questão, imagem e referência ao quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=255)
    question_image = models.ImageField(upload_to='quiz/question_images/', blank=True, null=True)

class Result(models.Model):
    """
    Modelo que representa um resultado possível de um quiz.
    Armazena nome, descrição, imagem e referência ao quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    result_image = models.ImageField(upload_to='quiz/result_images/', blank=True, null=True)

    def __str__(self):
        """
        Retorna uma descrição do resultado.

        :return: Texto descritivo do resultado.
        :rtype: str
        """
        return f"Quiz: {self.quiz.title}\n{self.name}\n{self.description}"
    
class Option(models.Model):
    """
    Modelo que representa uma opção de resposta para uma questão.
    Armazena texto, imagem e referência à questão.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=300)
    option_image = models.ImageField(upload_to='quiz/option_images/', blank=True, null=True)

    def __str__(self):
        """
        Retorna o texto da opção.

        :return: Texto da opção.
        :rtype: str
        """
        return f"{self.text}"


class OptionScore(models.Model):
    """
    Modelo que relaciona uma opção, um resultado e a pontuação atribuída.
    Armazena a pontuação de cada opção para cada resultado.
    """

    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="scores")
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="scores")
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ('option', 'result')

    def __str__(self):
        """
        Retorna o texto da opção, nome do resultado e pontos.

        :return: Texto descritivo da pontuação.
        :rtype: str
        """
        return f"{self.option.text} -> {self.result.name}: {self.points} pts"

