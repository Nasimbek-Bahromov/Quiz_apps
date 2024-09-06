from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .import models
from .models import Quiz, Question, Option, AnswerDetail, Answer, User
from random import choice
import openpyxl
from django.http import HttpResponse

from reportlab.pdfgen import canvas

def index(request):
    return render(request, 'index.html')


def quizList(request):
    images = [
        'https://st2.depositphotos.com/2769299/7314/i/450/depositphotos_73146775-stock-photo-a-stack-of-books-on.jpg',
        'https://img.freepik.com/free-photo/creative-composition-world-book-day_23-2148883765.jpg',
        'https://profit.pakistantoday.com.pk/wp-content/uploads/2018/04/Stack-of-books-great-education.jpg',
        'https://live-production.wcms.abc-cdn.net.au/73419a11ea13b52c6bd9c0a69c10964e?impolicy=wcms_crop_resize&cropH=1080&cropW=1918&xPos=1&yPos=0&width=862&height=485',
        'https://live-production.wcms.abc-cdn.net.au/398836216839841241467590824c5cf1?impolicy=wcms_crop_resize&cropH=2813&cropW=5000&xPos=0&yPos=0&width=862&height=485',
        'https://images.theconversation.com/files/45159/original/rptgtpxd-1396254731.jpg?ixlib=rb-4.1.0&q=45&auto=format&w=1356&h=668&fit=crop'
    ]
    
    quizes = models.Quiz.objects.filter(author=request.user)

    quizes_list = []

    for quiz in quizes:
        quiz.img = choice(images)
        quizes_list.append(quiz)

    return render(request, 'quiz-list.html', {'quizes': quizes_list, })

def quizDetail(request, id):
    quiz = get_object_or_404(models.Quiz, id=id)
    count = len(get_users_for_quiz(quiz_id = quiz.id))
    return render(request, 'quiz-detail.html', {'quiz': quiz, 'count':count})

def createQuiz(request):
    if request.method == 'POST':
        quiz = models.Quiz.objects.create(
            name=request.POST['name'],
            amount=request.POST['amount'],
            author=request.user
        )
        return redirect('quizDetail', quiz.id)
    return render(request, 'quiz-create.html')

def questionCreate(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        question_name = request.POST.get('question_name')
        options = request.POST.getlist('options[]')
        correct_option_index = int(request.POST.get('correct_option', -1))

        question = Question.objects.create(name=question_name, quiz=quiz)

        for index, option_text in enumerate(options):
            is_correct = (index == correct_option_index) 
            Option.objects.create(name=option_text, question=question, correct=is_correct)

        return redirect('quizDetail', id=quiz_id)

    return render(request, 'question-create.html', {'quiz_id': quiz_id})

def questionDetail(request, id):
    question = get_object_or_404(models.Question, id=id)
    options = models.Option.objects.filter(question=question)
    return render(request, 'question-detail.html', {'question': question, 'options': options})

def questionList(request):
    questions = models.Question.objects.all()
    return render(request, 'question-list.html', {'questions': questions})



@require_POST
def questionDelete(request, id):
    question = get_object_or_404(Question, id=id)
    question.delete()
    return redirect('quizDetail', id=question.quiz.id)

def get_users_for_quiz(quiz_id):
    # Belirlangan quizga tegishli javoblarni olish
    answers = Answer.objects.filter(quiz_id=quiz_id)
    
    # Qatnashgan foydalanuvchilarni olish
    users = User.objects.filter(answer__in=answers).distinct()
    
    return users

def quiz_users_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Quizga qatnashgan barcha foydalanuvchilar
    answers = Answer.objects.filter(quiz=quiz)
    
    results = []
    
    for answer in answers:
        answer_details = AnswerDetail.objects.filter(answer=answer)
        
        user_results = []
        for detail in answer_details:
            user_results.append({
                'question': detail.question.name,
                'correct_option': detail.question.correct_option.name if detail.question.correct_option else 'No option',
                'user_choice': detail.user_choice.name,
                'is_correct': detail.is_correct
            })
        
        results.append({
            'user': answer.author.username,
            'results': user_results
        })
    
    context = {
        'quiz': quiz,
        'results': results
    }
    return render(request, 'quiz_users.html', context)



def export_quiz_answers_to_excel(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    answers = Answer.objects.filter(quiz=quiz)
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Answers'
    
    
    sheet['A1'] = 'Author'
    sheet['B1'] = 'Start Time'
    sheet['C1'] = 'End Time'
    sheet['D1'] = 'Is Late?'

    for idx, answer in enumerate(answers, start=2):
        sheet[f'A{idx}'] = answer.author.username
        sheet[f'B{idx}'] = answer.start_time.strftime("%Y-%m-%d %H:%M:%S") if answer.start_time else ''
        sheet[f'C{idx}'] = answer.end_time.strftime("%Y-%m-%d %H:%M:%S") if answer.end_time else ''
        sheet[f'D{idx}'] = 'Yes' if answer.is_late else 'No'

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={quiz.name}_answers.xlsx'
    workbook.save(response)
    
    return response

def export_answer_detail_to_excel(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    answer_details = answer.answerdetail_set.all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Answer Details'

    
    sheet['A1'] = 'Question'
    sheet['B1'] = 'User Choice'
    sheet['C1'] = 'Correct?'

    for idx, detail in enumerate(answer_details, start=2):
        sheet[f'A{idx}'] = detail.question.name
        sheet[f'B{idx}'] = detail.user_choice.name
        sheet[f'C{idx}'] = 'Yes' if detail.is_correct else 'No'

   
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={answer.quiz.name}_answer_details.xlsx'
    workbook.save(response)

    return response



def render_quiz_to_pdf(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    answers = Answer.objects.filter(quiz=quiz)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={quiz.name}_results.pdf'

    p = canvas.Canvas(response)

    p.drawString(100, 800, f"Quiz Name: {quiz.name}")
    p.drawString(100, 780, f"Author: {quiz.author.username}")
    p.drawString(100, 760, "Results:")

    y = 740
    for answer in answers:
        p.drawString(100, y, f"{answer.author.username}: {'Late' if answer.is_late else 'On Time'}")
        y -= 20

    p.showPage()
    p.save()

    return response
