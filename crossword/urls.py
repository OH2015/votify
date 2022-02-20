from django.urls import path
from . import views

app_name='crossword'
urlpatterns = [
    path('', views.get_index, name='index'),
    path('search', views.search, name='search'),
]
