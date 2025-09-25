from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        label="Nome de usuário",
        error_messages={
            'unique': "Este nome de usuário já está em uso.",
            'required': "Por favor, informe um nome de usuário.",
        }
    )
    first_name = forms.CharField(
        label="Nome",
        error_messages={
            'required': "O nome é obrigatório.",
        }
    )
    last_name = forms.CharField(
        label="Sobrenome",
        error_messages={
            'required': "O sobrenome é obrigatório.",
        }
    )
    email = forms.EmailField(
        label="E-mail",
        error_messages={
            'unique': "Este e-mail já está em uso.",
            'required': "O e-mail é obrigatório.",
            'invalid': "Digite um endereço de e-mail válido.",
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Senha",
        error_messages={
            'required': "A senha é obrigatória.",
        }
    )
    profile_picture = forms.ImageField(
        label="Foto de perfil",
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
