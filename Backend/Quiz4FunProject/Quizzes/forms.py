from django import forms
from .models import *

class QuizForm(forms.ModelForm):
    """
    Formulário para criação/edição de Quiz.
    Permite criar ou editar quizzes, incluindo título, descrição e imagem principal.
    Herda de ModelForm do Django.
    """
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'quiz_main_picture']

class QuestionForm(forms.ModelForm):
    """
    Formulário para criação/edição de Questão.
    Permite criar ou editar questões de um quiz, incluindo texto e imagem.
    Herda de ModelForm do Django.
    """
    class Meta:
        model = Question
        fields = ['text', 'question_image']


class OptionForm(forms.ModelForm):
    """
    Formulário para criação/edição de Opção de resposta.
    Permite criar ou editar opções de resposta para uma questão, incluindo texto e imagem.
    Herda de ModelForm do Django.
    """
    class Meta:
        model = Option
        fields = ['text', 'option_image']


class ResultForm(forms.ModelForm):
    """
    Formulário para criação/edição de Resultado.
    Permite criar ou editar resultados possíveis de um quiz, incluindo nome, descrição e imagem.
    Herda de ModelForm do Django.
    """
    class Meta:
        model = Result
        fields = ['name', 'description', 'result_image']

class QuizSetupForm(forms.Form):
    """
    Formulário para configuração inicial de um Quiz.
    Permite definir quantidade de resultados, perguntas, opções por pergunta e se opções terão imagens.
    Herda de Form do Django.
    """
    num_results = forms.IntegerField(label="Number of results", min_value=2)
    num_questions = forms.IntegerField(label="Number of questions", min_value=1)
    num_options_per_question = forms.IntegerField(label="Number of options per question", min_value=2)
    options_have_images = forms.ChoiceField(
        label="Options have images?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect
    )