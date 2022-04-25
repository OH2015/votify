from django import forms

from .models import Question,Choice
from django.contrib.auth.models import User
from .models import Account

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', )

class ChoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs['hidden'] = True    # This is the solution
        # Setting as 'readonly' didn't make a difference
        # Setting as 'disabled' made the form not update the database


    class Meta:
        model =  Choice
        
        fields = ('question','choice_text', )




# Djangoユーザ
class AccountForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','email','password')
        # フィールド名指定
        labels = {'username':"ユーザーID",'email':"メール"}

# カスタムユーザ
class AddAccountForm(forms.ModelForm):
    class Meta():
        # モデルクラスを指定
        model = Account
        fields = ('last_name','first_name','account_image',)
        labels = {'last_name':" 姓",'first_name':"名",'account_image':"プロフィール画像",}