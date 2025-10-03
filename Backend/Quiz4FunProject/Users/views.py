from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import User
from django.core.mail import send_mail
from django.conf import settings
import secrets
from django.contrib.auth.hashers import make_password
from .auth.email_auth_form import EmailAuthenticationForm
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

def register_user(request):
    """
    Lida com o cadastro de um novo usuário.
    Se for uma requisição POST, valida e salva o formulário, envia e-mail de ativação e trata erros de integridade.
    Caso contrário, exibe o formulário vazio.

    :param request: Objeto HttpRequest que contém os dados da requisição (POST ou GET).
    :type request: django.http.HttpRequest
    :return: HttpResponse com o formulário renderizado ou HttpResponseRedirect para login.
    :rtype: django.http.HttpResponse ou django.http.HttpResponseRedirect
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.password = make_password(form.cleaned_data['password'])
                user.is_active = False
                user.activation_token = secrets.token_urlsafe(32)
                user.save()
                activation_link = f"{settings.SITE_DOMAIN}/users/activate/{user.activation_token}/"
                send_mail(
                    'Ative sua conta Quiz4Fun',
                    f'Olá {user.first_name},\n\nClique no link para ativar sua conta: {activation_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.warning(request, 'Cadastro realizado! Verifique seu e-mail para ativar sua conta.')
                return redirect('users:login_user')
            except IntegrityError:
                messages.error(request, "Este e-mail já está em uso.")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def activate_user(request, token):
    """
    Ativa a conta do usuário utilizando o token recebido por e-mail.
    Caso o token seja válido, ativa o usuário e exibe mensagem de sucesso. Caso contrário, exibe mensagem de erro.

    :param request: Objeto HttpRequest que contém os dados da requisição.
    :type request: django.http.HttpRequest
    :param token: Token de ativação recebido por e-mail.
    :type token: str
    :return: HttpResponseRedirect para login, com mensagem de sucesso ou erro.
    :rtype: django.http.HttpResponseRedirect
    """
        try:
            user = User.objects.get(activation_token=token)
            user.is_active = True
            user.activation_token = None
            user.save()
            messages.success(request, 'Conta ativada com sucesso! Você pode fazer login.')
            return redirect('users:login_user')
        except User.DoesNotExist:
            messages.error(request, 'Token de ativação inválido ou expirado.')
            return redirect('users:login_user')

def login_user(request):
    """
    Lida com o login do usuário.
    Se o usuário já estiver autenticado, redireciona para o menu de quizzes.
    Se for uma requisição POST, valida o formulário e autentica o usuário, exibindo mensagens de erro conforme necessário.
    Caso contrário, exibe o formulário de login.

    :param request: Objeto HttpRequest que contém os dados da requisição (POST ou GET).
    :type request: django.http.HttpRequest
    :return: HttpResponse com o formulário renderizado ou HttpResponseRedirect para o menu de quizzes.
    :rtype: django.http.HttpResponse ou django.http.HttpResponseRedirect
    """
    if request.user.is_authenticated:
        return redirect('quizzes:quiz_menu')

    form = EmailAuthenticationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if not user.is_active:
                    return render(request, 'users/login.html', {'form': form, 'error': 'Conta não ativada. Verifique seu e-mail.'})
                login(request, user)
                return redirect('quizzes:quiz_menu')
            else:
                return render(request, 'users/login.html', {'form': form, 'error': 'E-mail ou senha incorretos.'})
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    """
    Realiza o logout do usuário e redireciona para a página de login.

    :param request: Objeto HttpRequest da requisição.
    :type request: django.http.HttpRequest
    :return: HttpResponseRedirect para a página de login.
    :rtype: django.http.HttpResponseRedirect
    """
    logout(request)
    return redirect('users:login_user')

@login_required(login_url='/users/login/')
def user_status(request):
    """
    Exibe a página de status do usuário logado.

    :param request: Objeto HttpRequest da requisição.
    :type request: django.http.HttpRequest
    :return: HttpResponse com a página de status do usuário.
    :rtype: django.http.HttpResponse
    """
    return render(request, 'users/status.html')

class UserPasswordResetView(auth_views.PasswordResetView):
    """
    View para solicitação de redefinição de senha do usuário.
    Renderiza o formulário de solicitação e envia e-mail de redefinição.
    """
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    View que exibe confirmação de envio do e-mail de redefinição de senha.
    """
    template_name = "users/password_reset_done.html"

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    View para confirmação de redefinição de senha do usuário.
    Renderiza o formulário para definir nova senha.
    """
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """
    View que exibe confirmação de redefinição de senha concluída.
    """
    template_name = "users/password_reset_complete.html"