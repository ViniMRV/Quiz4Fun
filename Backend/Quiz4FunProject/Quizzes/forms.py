from django import forms
from .models import *

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'quiz_main_picture']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_image']


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text', 'option_image']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['name', 'description', 'result_image']

class QuizSetupForm(forms.Form):
    num_results = forms.IntegerField(label="Number of results", min_value=2)
    num_questions = forms.IntegerField(label="Number of questions", min_value=1)
    num_options_per_question = forms.IntegerField(label="Number of options per question", min_value=2)
    options_have_images = forms.ChoiceField(
        label="Options have images?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect
    )