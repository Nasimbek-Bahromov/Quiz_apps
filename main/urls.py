from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.index, name='index'),
    path('', views.quizList, name='quizList'),
    path('quiz-detail/<int:id>/', views.quizDetail, name='quizDetail'),
    path('create-quiz/', views.createQuiz, name='createQuiz'),
    path('question-detail/<int:id>/', views.questionDetail, name='question_detail'),
    path('question-list/', views.questionList, name='question_list'),
    path('question-create/<int:quiz_id>/', views.questionCreate, name='question_create'),
    path('question/delete/<int:id>/', views.questionDelete, name='question_delete'),
    path('quiz/detail/<int:quiz_id>/users/', views.quiz_users_view, name='quiz_users'),
]
