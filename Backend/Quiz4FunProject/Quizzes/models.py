from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name="quizzes")
    quiz_main_picture = models.ImageField(upload_to='quiz/main_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=255)
    question_image = models.ImageField(upload_to='quiz/question_images/', blank=True, null=True)

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    result_image = models.ImageField(upload_to='quiz/result_images/', blank=True, null=True)

    def __str__(self):
        return f'''
                Quiz: {self.quiz.title}

                {self.name}
                {self.description}
                '''
    
class Option(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=300)
    option_image = models.ImageField(upload_to='quiz/option_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.text}"


class OptionScore(models.Model):

    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="scores")
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="scores")
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ('option', 'result')

    def __str__(self):
        return f"{self.option.text} -> {self.result.name}: {self.points} pts"

