from django import forms

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
