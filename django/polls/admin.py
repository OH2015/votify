from django.contrib import admin
from .models import Question,Choice,Comment, UpdateContent, Vote
from django.contrib.auth import get_user_model


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class CommentInline(admin.TabularInline):
    model = Comment


# Register your models here.
admin.site.register(Question)
admin.site.register(get_user_model())
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(UpdateContent)

    
