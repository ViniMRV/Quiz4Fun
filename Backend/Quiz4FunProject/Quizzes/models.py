from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=255)

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'''
                Quiz: {self.quiz.title}

                {self.name}
                {self.description}
                '''
    
class Option(models.Model):
    """
    Tabela de opções para uma pergunta.
    Representa as possíveis respostas para uma pergunta do quiz.
    Cada opção está associada a uma pergunta específica e contém um texto descritivo.
    As opções são usadas para calcular os resultados com base nas respostas dos usuários.
    Cada opção pode ter uma pontuação associada a diferentes resultados.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.text}"


class OptionScore(models.Model):
    """
    Tabela intermediária: 
    Cada opção ganha pontos diferentes para cada resultado.
    """
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="scores")
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="scores")
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ('option', 'result')

    def __str__(self):
        return f"{self.option.text} -> {self.result.name}: {self.points} pts"

