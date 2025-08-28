

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import User
from django.core.mail import send_mail
from django.conf import settings
import secrets
from django.contrib.auth.hashers import make_password

def register_user(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save(commit=False)
			user.password = make_password(form.cleaned_data['password'])
			user.is_active = False
			user.activation_token = secrets.token_urlsafe(32)
			user.save()
			activation_link = request.build_absolute_uri(f"/users/activate/{user.activation_token}/")
			send_mail(
				'Ative sua conta Quiz4Fun',
				f'Olá {user.first_name},\n\nClique no link para ativar sua conta: {activation_link}',
				settings.DEFAULT_FROM_EMAIL,
				[user.email],
				fail_silently=False,
			)
			return redirect('activation_email_sent')
	else:
		form = UserRegistrationForm()
	return render(request, 'users/register.html', {'form': form})
def activate_user(request, token):
	try:
		user = User.objects.get(activation_token=token)
		user.is_active = True
		user.activation_token = None
		user.save()
		return render(request, 'users/activation_success.html')
	except User.DoesNotExist:
		return render(request, 'users/activation_failed.html')

def login_user(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			if not user.is_active:
				return render(request, 'login.html', {'form': form, 'error': 'Conta não ativada. Verifique seu e-mail.'})
			login(request, user)
			return redirect('user_status')
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})

def logout_user(request):
	logout(request)
	return redirect('login_user')

@login_required(login_url='/users/login/')
def user_status(request):
	return render(request, 'status.html')
