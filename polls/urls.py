from urllib import request
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/edit_question/', views.edit_question, name='edit_question'),
    path('<int:pk>/edit_choice/', views.edit_choice, name='edit_choice'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('update_history/', views.UpdateHistory, name='update_history'),
    
    path('create_question/', views.create_question, name='create_question'),
    path('<int:pk>/create_choice/', views.create_choice, name='create_choice'),
]