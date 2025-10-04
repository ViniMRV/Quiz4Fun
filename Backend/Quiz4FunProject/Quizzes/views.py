from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import get_object_or_404
from .models import *
from django.forms import modelform_factory
from Users.models import UserQuizResult
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class UserQuizzesView(View):
    """
    Exibe os quizzes do usuário logado.

    :param request: HttpRequest com usuário autenticado.
    :return: HttpResponse com a lista de quizzes.
    """
    def get(self, request, *args, **kwargs):
        quizzes = request.user.quizzes.all()
        return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class QuizMenuView(View):
    """
    Exibe o menu principal de quizzes.

    :param request: HttpRequest com usuário autenticado.
    :return: HttpResponse com o menu de quizzes.
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'quizzes/quiz_menu.html')

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class CreateQuizView(View):
    """
    Lida com a criação de um novo quiz. 
    Se for uma requisição POST, valida e salva o formulário, vinculando o quiz ao usuário logado.
    Caso contrário, exibe o formulário vazio.

    :param request: Objeto HttpRequest que contém os dados da requisição (POST ou GET).
    :type request: django.http.HttpRequest
    :return: HttpResponse com o formulário renderizado ou HttpResponseRedirect para a configuração do quiz.
    :rtype: django.http.HttpResponse ou django.http.HttpResponseRedirect
    """
    def get(self, request, *args, **kwargs):
        form = QuizForm()
        return render(request, 'quizzes/create_quiz.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('quizzes:quiz_setup', quiz_id=quiz.id)
        return render(request, 'quizzes/create_quiz.html', {'form': form})

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class QuizSetupView(View):
    """
    Lida com a configuração de perguntas e resultados de um quiz.
    Se for uma requisição POST, processa os dados do formulário e salva a configuração.
    Caso contrário, exibe o formulário de configuração inicial.

    :param request: Objeto HttpRequest que contém os dados da requisição (POST ou GET).
    :type request: django.http.HttpRequest
    :param quiz_id: ID do quiz a ser configurado.
    :type quiz_id: int
    :return: HttpResponse com o formulário renderizado ou HttpResponseRedirect para adicionar resultados.
    :rtype: django.http.HttpResponse ou django.http.HttpResponseRedirect
    """
    def get(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
        return render(request, 'quizzes/quiz_setup.html', {
            'quiz': quiz,
            'show_questions_setup': False,
        })

    def post(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)

        if 'set_questions' in request.POST:
            num_questions = int(request.POST.get('num_questions', 1))
            num_results = int(request.POST.get('num_results', 2))
            question_range = range(num_questions)

            return render(request, 'quizzes/quiz_setup.html', {
                'quiz': quiz,
                'num_questions': num_questions,
                'num_results': num_results,
                'question_range': question_range,
                'show_questions_setup': True,
            })
        else:
            num_questions = int(request.POST.get('num_questions', 1))
            num_results = int(request.POST.get('num_results', 2))

            questions_setup = []
            for q_idx in range(num_questions):
                num_options = int(request.POST.get(f'q{q_idx}_num_options', 2))
                options_have_images = request.POST.get(f'q{q_idx}_options_have_images', 'no') == 'yes'
                questions_setup.append({
                    'num_options': num_options,
                    'options_have_images': options_have_images
                })

            request.session[f'quiz_{quiz_id}_setup'] = {
                'num_questions': num_questions,
                'num_results': num_results,
                'questions_setup': questions_setup
            }

            return redirect('quizzes:add_results', quiz_id=quiz.id)

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class AddResultsView(View):
    """
    Lida com a adição de resultados ao quiz.
    Se for uma requisição POST, valida e salva os resultados, redirecionando para adicionar perguntas.
    Caso contrário, exibe o formulário para cada resultado.

    :param request: Objeto HttpRequest que contém os dados da requisição (POST ou GET).
    :type request: django.http.HttpRequest
    :param quiz_id: ID do quiz.
    :type quiz_id: int
    :return: HttpResponse com o formulário renderizado ou HttpResponseRedirect para adicionar perguntas.
    :rtype: django.http.HttpResponse ou django.http.HttpResponseRedirect
    """
    def get(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
        setup = request.session.get(f'quiz_{quiz_id}_setup')
        num_results = setup.get('num_results', 2)

        ResultForm = modelform_factory(Result, fields=['name', 'description', 'result_image'])
        forms = [ResultForm(prefix=str(i)) for i in range(num_results)]
        return render(request, 'quizzes/add_results.html', {'quiz': quiz, 'forms': forms})

    def post(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
        setup = request.session.get(f'quiz_{quiz_id}_setup')
        num_results = setup.get('num_results', 2)

        ResultForm = modelform_factory(Result, fields=['name', 'description', 'result_image'])
        forms = [ResultForm(request.POST, request.FILES, prefix=str(i)) for i in range(num_results)]
        if all(f.is_valid() for f in forms):
            for f in forms:
                result = f.save(commit=False)
                result.quiz = quiz
                result.save()
            return redirect('quizzes:add_questions', quiz_id=quiz.id)

        return render(request, 'quizzes/add_results.html', {'quiz': quiz, 'forms': forms})

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class AddQuestionsView(View):
    """
    Lida com a adição de perguntas e opções ao quiz.
    Se for uma requisição POST, valida e salva perguntas, opções e pontuações, finalizando a criação do quiz.
    Caso contrário, exibe os formulários para cada pergunta e suas opções.

    :param request: Objeto HttpRequest que contém os dados da requisição (POST ou GET).
    :type request: django.http.HttpRequest
    :param quiz_id: ID do quiz.
    :type quiz_id: int
    :return: HttpResponse com o formulário renderizado ou HttpResponseRedirect para finalizar o quiz.
    :rtype: django.http.HttpResponse ou django.http.HttpResponseRedirect
    """
    def get(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
        setup = request.session.get(f'quiz_{quiz_id}_setup')

        if not setup:
            return redirect('quizzes:quiz_setup', quiz_id=quiz.id)

        questions_setup = setup.get('questions_setup', [])
        QuestionForm = modelform_factory(Question, fields=['text', 'question_image'])

        questions_with_options = []
        for q_idx, q_setup in enumerate(questions_setup):
            q_form = QuestionForm(prefix=f'q{q_idx}')
            fields = ['text']
            if q_setup.get('options_have_images', False):
                fields.append('option_image')
            OptionForm = modelform_factory(Option, fields=fields)
            options = [OptionForm(prefix=f'q{q_idx}_opt{o_idx}') for o_idx in range(q_setup.get('num_options', 2))]
            questions_with_options.append({
                'q_form': q_form,
                'options': options
            })

        return render(request, 'quizzes/add_questions.html', {
            'quiz': quiz,
            'questions_with_options': questions_with_options,
            'results': quiz.results.all()
        })

    def post(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
        setup = request.session.get(f'quiz_{quiz_id}_setup')
        questions_setup = setup.get('questions_setup', [])

        # Formulário de perguntas
        QuestionForm = modelform_factory(Question, fields=['text', 'question_image'])
        option_forms_per_question = []
        for q_setup in questions_setup:
            fields = ['text']
            if q_setup.get('options_have_images', False):
                fields.append('option_image')
            OptionForm = modelform_factory(Option, fields=fields)
            option_forms_per_question.append(OptionForm)

        # Itera pelas perguntas configuradas
        for q_idx, q_setup in enumerate(questions_setup):
            q_form = QuestionForm(request.POST, request.FILES, prefix=f'q{q_idx}')
            OptionForm = option_forms_per_question[q_idx]
            option_forms = [
                OptionForm(request.POST, request.FILES, prefix=f'q{q_idx}_opt{o_idx}')
                for o_idx in range(q_setup.get('num_options', 2))
            ]

            # Verifica se os formulários são válidos
            if not (q_form.is_valid() and all(of.is_valid() for of in option_forms)):
                print(f"[ERRO] Questão {q_idx} inválida:")
                print("Erros da questão:", q_form.errors)
                for o_idx, of in enumerate(option_forms):
                    if of.errors:
                        print(f"Erros da opção {o_idx}:", of.errors)
                continue  # Pula só esta questão, segue para a próxima

            # Salva a questão
            question = q_form.save(commit=False)
            question.quiz = quiz
            question.save()

            # Salva as opções e suas pontuações
            for o_idx, of in enumerate(option_forms):
                option = of.save(commit=False)
                option.question = question
                option.save()

                for result in quiz.results.all():
                    key = f'q{q_idx}_opt{o_idx}_points_{result.id}'
                    points = int(request.POST.get(key, 0))
                    OptionScore.objects.create(option=option, result=result, points=points)

        # Debug: imprime no console as pontuações salvas
        print("Pontos salvos:")
        for option in Option.objects.filter(question__quiz=quiz):
            for score in option.scores.all():
                print(option.text, score.result.name, score.points)

        return redirect('quizzes:user_quizzes')

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class TakeQuizView(View):
    """
    Lida com a participação do usuário em um quiz.
    Se for uma requisição POST, calcula o resultado e salva a resposta do usuário, redirecionando para a página de resultado.
    Caso contrário, exibe as perguntas do quiz para o usuário responder.

    :param request: Objeto HttpRequest que contém os dados da requisição (POST ou GET).
    :type request: django.http.HttpRequest
    :param quiz_id: ID do quiz.
    :type quiz_id: int
    :return: HttpResponse com o formulário renderizado ou HttpResponseRedirect para o resultado.
    :rtype: django.http.HttpResponse ou django.http.HttpResponseRedirect
    """
    def get(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        existing_result = UserQuizResult.objects.filter(user=request.user, quiz=quiz).first()
        if existing_result:
            return redirect('quizzes:quiz_result', quiz_id=quiz.id)

        return render(request, 'quizzes/take_quiz.html', {
            'quiz': quiz,
            'questions': quiz.questions.all(),
        })

    def post(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        selected_options = [int(request.POST.get(f'question_{q.id}')) for q in quiz.questions.all() if request.POST.get(f'question_{q.id}')]

        result_scores = {r.id: 0 for r in quiz.results.all()}
        for option_id in selected_options:
            option = Option.objects.get(id=option_id)
            for score in option.scores.all():
                result_scores[score.result.id] += score.points

        best_result_id = max(result_scores, key=result_scores.get)
        best_result = Result.objects.get(id=best_result_id)

        UserQuizResult.objects.create(user=request.user, quiz=quiz, result=best_result)
        return redirect('quizzes:quiz_result', quiz_id=quiz.id)

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class QuizResultView(View):
    """
    Exibe o resultado do quiz para o usuário logado.
    Renderiza a página de resultado do quiz para o usuário.

    :param request: Objeto HttpRequest que contém os dados da requisição.
    :type request: django.http.HttpRequest
    :param quiz_id: ID do quiz.
    :type quiz_id: int
    :return: HttpResponse com o resultado do quiz.
    :rtype: django.http.HttpResponse
    """
    def get(self, request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        user_result = get_object_or_404(UserQuizResult, user=request.user, quiz=quiz)

        return render(request, 'quizzes/quiz_result.html', {
            'quiz': quiz,
            'user_result': user_result,
        })

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class QuizListView(View):
    """
    Exibe a lista de todos os quizzes disponíveis.
    """
    def get(self, request, *args, **kwargs):
        quizzes = Quiz.objects.all().select_related("created_by")
        return render(request, "quizzes/quiz_list.html", {"quizzes": quizzes})