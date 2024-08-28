from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz-list/', views.quizList, name='quizList'),
    path('quiz-detail/<int:id>/', views.quizDetail, name='quizDetail'),
    path('create-quiz/', views.createQuiz, name='createQuiz'),
    path('question-detail/<int:id>/', views.questionDetail, name='questionDetail'),
    path('question-list/', views.questionList, name='question_list'),
    path('question-create/<int:quiz_id>/', views.questionCreate, name='question_create'),
    path('question/delete/<int:id>/', views.questionDelete, name='question_delete'),
]
