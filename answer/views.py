from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Quiz, Question, Option, Answer, AnswerDetail
from django.utils import timezone

def getQuiz(request, id):
    quiz = Quiz.objects.get(id=id)
    return render(request, 'answer/get-quiz.html', {'quiz':quiz})

def makeAnswer(request, id):
    quiz = Quiz.objects.get(id=id)
    answer = Answer.objects.create(quiz=quiz, author=request.user)
    for key, value in request.POST.items():
        if key.isdigit():
            answer =answer,
            question = Question.objects.get(id = int(key))
            user_choise = Option.objects.get(id = int(value))
    return redirect('getQuiz', quiz.id)



@login_required
def check_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user

    answer, created = Answer.objects.get_or_create(quiz=quiz, author=user)

    if created:
        answer.start_time = timezone.now()

    AnswerDetail.objects.filter(answer=answer).delete()

    for question in quiz.questions:
        selected_option_id = request.POST.get(f'question_{question.id}')

        if selected_option_id:
            selected_option = get_object_or_404(Option, id=selected_option_id)

            answer_detail = AnswerDetail(
                answer=answer,
                question=question,
                user_choice=selected_option,
                correct=selected_option.correct
            )
            answer_detail.save()

    answer.end_time = timezone.now()
    answer.save()


    return redirect('result_detail', quiz_id=quiz.id)

def result(request):
    results = []
    quizzes = Quiz.objects.filter(author=request.user)
    
    for quiz in quizzes:
        total_questions = quiz.questions_count
        answer_details = AnswerDetail.objects.filter(answer__quiz=quiz)
        correct_answers_count = answer_details.filter(correct=True).count()
        incorrect_answers_count = answer_details.count() - correct_answers_count

        p = correct_answers_count / total_questions * 100

        results.append({
            'quiz': quiz,
            'questions_count': total_questions,
            'correct_answers_count': correct_answers_count,
            'incorrect_answers_count': incorrect_answers_count,
            'p': p,
        })

    return render(request, 'result.html', {'results': results, 'quizes':quizzes})

def result_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    answer = Answer.objects.get(quiz=quiz, author=request.user)
    answer_details = AnswerDetail.objects.filter(answer=answer)

    correct_count = 0
    total_questions = answer_details.count()
    results = []

    for detail in answer_details:
        is_correct = detail.is_correct
        if is_correct:
            correct_count += 1
        results.append({
            'question': detail.question,
            'user_choice': detail.user_choice,
            'is_correct': is_correct,
            'correct': detail.question.correct_option.name,
        })

    if total_questions > 0:
        correct_percentage = (correct_count / total_questions) * 100
    else:
        correct_percentage = 0 

    context = {
        'quiz': quiz,
        'results': results,
        'p': correct_percentage,
    }
    return render(request, 'result_detail.html', context)


