from django.contrib import admin
from .models import Question,Choice
from .models import Account

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Date information', {'fields': ['author'], 'classes': ['collapse']}),
    ]
    list_display = ('title', 'was_published_recently')
    
    search_fields = ['title']
    inlines = [ChoiceInline]

# Register your models here.
admin.site.register(Question,QuestionAdmin)
admin.site.register(Account)
