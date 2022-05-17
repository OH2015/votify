from django import forms

from .models import Question,Choice
from django.contrib.auth.models import User
from .models import Account

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', )

class ChoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs['hidden'] = True    # This is the solution
        # Setting as 'readonly' didn't make a difference
        # Setting as 'disabled' made the form not update the database


    class Meta:
        model =  Choice
        
        fields = ('question','choice_text', )
