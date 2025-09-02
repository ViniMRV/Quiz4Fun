
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Users.models import UserQuiz


# View para mostrar quizzes do usuário autenticado
@login_required(login_url='/users/login/')
def user_quizzes(request):
	user = request.user
	user_quizzes = UserQuiz.objects.filter(user=user).select_related('quiz')
	quizzes = [uq.quiz for uq in user_quizzes]
	return render(request, 'quizzes/user_quizzes.html', {'quizzes': quizzes})

