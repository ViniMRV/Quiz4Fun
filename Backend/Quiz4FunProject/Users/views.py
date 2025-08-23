
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def register_user(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('register_user')  # Redireciona para a mesma página ou para login
	else:
		form = UserRegistrationForm()
	return render(request, 'users/register.html', {'form': form})
