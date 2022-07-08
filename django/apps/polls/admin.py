from dataclasses import fields
from django.contrib import admin
from .models import Genre, Question,Choice,Comment, Vote
from .models import Account


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class CommentInline(admin.TabularInline):
    model = Comment


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title']
    
    search_fields = ['title']
    inlines = [ChoiceInline,CommentInline]


# Register your models here.
admin.site.register(Question,QuestionAdmin)
admin.site.register(Account)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Vote)

    
