from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, CustomPasswordResetForm
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
	logout(request)
	return redirect('users:login_user')

@login_required(login_url='/users/login/')
def user_status(request):
	return render(request, 'users/status.html')

class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")

    def form_valid(self, form):
        form.save(
            use_https=self.request.is_secure(),
            from_email=self.from_email,
            email_template_name=self.email_template_name,
            request=self.request,
            html_email_template_name=self.html_email_template_name,
            extra_email_context=self.extra_email_context,
            domain_override=settings.SITE_DOMAIN.replace("https://", "").replace("http://", ""),
        )
        return redirect(self.success_url)

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"