from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import get_object_or_404
from .models import *
from django.forms import modelform_factory

@login_required(login_url='/users/login/')
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('quizzes:quiz_setup', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quizzes/create_quiz.html', {'form': form})

@login_required(login_url='/users/login/')
def quiz_setup(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)

    if request.method == 'POST':
        if 'set_questions' in request.POST:
            # First submission: user sets the number of questions & results
            num_questions = int(request.POST.get('num_questions', 1))
            num_results = int(request.POST.get('num_results', 2))
            # Build a list for the template
            question_range = range(num_questions)

            return render(request, 'quizzes/quiz_setup.html', {
                'quiz': quiz,
                'num_questions': num_questions,
                'num_results': num_results,
                'question_range': question_range,
                'show_questions_setup': True,
            })
        else:
            # Second submission: user filled per-question settings
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

    # GET request or default rendering
    return render(request, 'quizzes/quiz_setup.html', {
        'quiz': quiz,
        'show_questions_setup': False,
    })

@login_required(login_url='/users/login/')
def add_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    setup = request.session.get(f'quiz_{quiz_id}_setup')
    num_results = setup.get('num_results', 2)

    ResultForm = modelform_factory(Result, fields=['name', 'description', 'result_image'])

    if request.method == 'POST':
        forms = [ResultForm(request.POST, request.FILES, prefix=str(i)) for i in range(num_results)]
        if all(f.is_valid() for f in forms):
            for f in forms:
                result = f.save(commit=False)
                result.quiz = quiz
                result.save()
            return redirect('quizzes:add_questions', quiz_id=quiz.id)
    else:
        forms = [ResultForm(prefix=str(i)) for i in range(num_results)]

    return render(request, 'quizzes/add_results.html', {'quiz': quiz, 'forms': forms})

@login_required(login_url='/users/login/')
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    setup = request.session.get(f'quiz_{quiz_id}_setup')

    if not setup:
        return redirect('quizzes:quiz_setup', quiz_id=quiz.id)

    questions_setup = setup.get('questions_setup', [])

    QuestionForm = modelform_factory(Question, fields=['text', 'question_image'])

    # Prepare OptionForm per question depending on image requirement
    option_forms_per_question = []
    for q_setup in questions_setup:
        fields = ['text']
        if q_setup.get('options_have_images', False):
            fields.append('option_image')
        OptionForm = modelform_factory(Option, fields=fields)
        option_forms_per_question.append(OptionForm)

    if request.method == 'POST':
        for q_idx, q_setup in enumerate(questions_setup):
            q_form = QuestionForm(request.POST, request.FILES, prefix=f'q{q_idx}')
            OptionForm = option_forms_per_question[q_idx]
            option_forms = [
                OptionForm(request.POST, request.FILES, prefix=f'q{q_idx}_opt{o_idx}')
                for o_idx in range(q_setup.get('num_options', 2))
            ]

            if q_form.is_valid() and all(of.is_valid() for of in option_forms):
                question = q_form.save(commit=False)
                question.quiz = quiz
                question.save()

                for o_idx, of in enumerate(option_forms):
                    option = of.save(commit=False)
                    option.question = question
                    option.save()

                    # Save points for each result
                    for result in quiz.results.all():
                        points = int(request.POST.get(f'q{q_idx}_opt{o_idx}_points_{result.id}', 0))
                        OptionScore.objects.create(option=option, result=result, points=points)

        return redirect('users:user_status')  # finish quiz creation

    else:
        # Prepare questions with their options for the template
        questions_with_options = []
        for q_idx, q_setup in enumerate(questions_setup):
            q_form = QuestionForm(prefix=f'q{q_idx}')
            OptionForm = option_forms_per_question[q_idx]
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

@login_required(login_url='/users/login/')
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        # Collect scores per result
        scores = {result.id: 0 for result in quiz.results.all()}

        for question in quiz.questions.all():
            selected_option_id = request.POST.get(f"question_{question.id}")
            if selected_option_id:
                option = Option.objects.get(id=selected_option_id)
                for option_score in option.optionscore_set.all():
                    scores[option_score.result.id] += option_score.points

        # Pick the top scoring result
        best_result_id = max(scores, key=scores.get)
        best_result = Result.objects.get(id=best_result_id)

        return render(request, "quizzes/quiz_result.html", {
            "quiz": quiz,
            "result": best_result,
            "score": scores[best_result_id],
        })

    # GET → show quiz
    return render(request, "quizzes/take_quiz.html", {
        "quiz": quiz,
        "questions": quiz.questions.all()
    })
