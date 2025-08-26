

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

def register_user(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('login_user')  # Redireciona para login após registro
	else:
		form = UserRegistrationForm()
	return render(request, 'users/register.html', {'form': form})

def login_user(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
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
