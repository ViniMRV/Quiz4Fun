from django import forms
from .models import User
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm

class UserRegistrationForm(forms.ModelForm):
    """
    Formulário para cadastro de usuário.
    Permite criar um novo usuário, incluindo validações customizadas e campo de foto de perfil.
    Herda de ModelForm do Django.
    """
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
        """
        Salva o usuário criado pelo formulário, usando senha criptografada.
        Sobrescreve o método save para garantir que a senha seja armazenada de forma segura.

        :param commit: Indica se o usuário deve ser salvo imediatamente no banco de dados.
        :type commit: bool
        :return: Instância do usuário criada pelo formulário.
        :rtype: Users.User
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CustomPasswordResetForm(PasswordResetForm):
    def save(self, domain_override=None, subject_template_name=None,
             email_template_name=None, use_https=False, token_generator=None,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        # Force your GitHub Codespaces domain
        domain_override = settings.SITE_DOMAIN
        use_https = True  # always https

        # Inject subject directly as string
        subject_template_name = None
        self.subject = "Redefinição de senha - Quiz4Fun"

        return super().save(
            domain_override=domain_override,
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            use_https=use_https,
            token_generator=token_generator,
            from_email=from_email,
            request=request,
            html_email_template_name=html_email_template_name,
            extra_email_context=extra_email_context,
        )
    
    