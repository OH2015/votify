from posixpath import split
from django.shortcuts import get_object_or_404, redirect, render
from .models import Account, Genre, Question,Choice,UpdateContent,Comment
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import TemplateView # テンプレートタグ
from rest_framework import generics
from .models import Question
from .serializers import ChoiceSerializer, QuestionSerializer, CommentSerializer
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core import serializers


# トップ画面
class IndexView(TemplateView):
    # これを書かなかったらデフォルトで「polls/Question_list.html」が探される
    template_name = 'polls/index.html'


# 投票画面
class Vote(TemplateView):
    # GET(pk:question_id)
    def get(self, request,pk):
        question = get_object_or_404(Question, pk=pk)
        # 閲覧回数をカウント
        question.watched += 1
        question.save()
        
        has_voted = str(pk) in request.session

        # テンプレートとパラメータを返却
        if has_voted:
            return render(request,"polls/detail.html",{'question': question})
        else:
            return render(request,"polls/vote.html",{'question': question,})

    def post(self,request,pk):
        choice = Choice.objects.get(id=request.POST['choice'])
        choice.votes += 1
        choice.save()

        # セッションに投票済み登録
        request.session[str(choice.question.id)] = "voted"
        return render(request,"polls/detail.html",{'question': get_object_or_404(Question, pk=pk)})

# コメント投稿API
class PostComment(TemplateView):
    def post(self,request,pk):
        Comment.objects.create(question_id=pk,user=request.user,text=request.POST.get('text'))
        return JsonResponse({})

# 更新履歴
def UpdateHistory(request):
    return render(request,"polls/update_history.html",{"contents":UpdateContent.objects.all})


# 投稿
@method_decorator(login_required, name='dispatch')
class CreateQuestion(TemplateView):
    def get(self,request):
        return render(request, 'polls/create.html', {'genres':Genre.objects.all()})

    def post(self,request):
        choice_num = request.POST['choice_num']
        genre = request.POST['genre']
        print(genre)
        if genre:
            genre = Genre.objects.get(title=genre) 
        else:
            genre = None
            
        question = Question.objects.create(title=request.POST['question_title'],explanation=request.POST['explanation'],genre=genre,author=request.user)
        for i in range(int(choice_num)):
            Choice.objects.create(choice_text=request.POST[f'choice_title{i}'],question=question)

        return redirect('polls:index')


# アカウント登録
class  AccountRegistration(TemplateView):
    def __init__(self):
        self.params = {"message":""}

    # Get処理
    def get(self,request):
        return render(request,"polls/register.html",context=self.params)

    # Post処理
    def post(self,request):
        id = request.POST.get('id')
        email = request.POST.get('email')
        pw = request.POST.get('pw')
        ln = request.POST.get('last_name')
        fn = request.POST.get('first_name')
        
        user = User.objects.create_user(id,email,pw)

        if user == None:
            self.params["message"] = "ユーザの作成に失敗しました"
            return render(request,"polls/register.html",context=self.params)
            
        acc = Account.objects.create(user=user,last_name=ln,first_name=fn)
        
        if acc == None:
            user.delete()
            self.params["message"] = "ユーザの作成に失敗しました"
            return render(request,"polls/register.html",context=self.params)

        self.params["message"] = "アカウントを作成しました"
        login(request,user)

        return render(request,"polls/register.html",context=self.params)


# マイページ
def mypage(request):
    acc = Account.objects.get(user=request.user)
    return render(request, 'polls/mypage.html',context={"account":acc})


# My投稿一覧
@method_decorator(login_required, name='dispatch')
class  MyQuestions(TemplateView):
    def get(self,request):
        user = request.user
        questions = Question.objects.filter(author=user).all()
        return render(request,"polls/my_questions.html",{"questions":questions})

# 
# API
# 


# Questionオブジェクトのリストを返すAPIビュー
class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()

    # 独自に拡張
    def list(self,request):
        keyword = request.query_params.get('keyword')

        # キーワードがあれば絞り込み
        if keyword:
            self.queryset = Question.objects.filter(title__contains=keyword).all()

        queryset = self.get_queryset()
        serializer = QuestionSerializer(queryset,many=True)
        return Response(serializer.data)

# 特定のQuestionオブジェクトの参照APIビュー
class QuestionRetrieveAPIView(generics.RetrieveAPIView):
    # 操作カスタマイズ
    def get(self,request,pk):
        # クエリー
        queryset = Question.objects.get(id=pk)
        serializer = QuestionSerializer(queryset)

        return Response(serializer.data)

# Choiceオブジェクトのリストを返すAPIビュー
class ChoiceListAPIView(generics.ListAPIView):
    # 独自に拡張
    def list(self,request,pk):
        if request.query_params.get('sort'):
            self.queryset = Choice.objects.order_by('-votes').filter(question_id=pk).all()
        else:
            self.queryset = Choice.objects.filter(question_id=pk).all()


        queryset = self.get_queryset()
        serializer = ChoiceSerializer(queryset, many=True)

        return Response(serializer.data)


# Commentオブジェクトのリストを返すAPIビュー
class CommentListAPIView(generics.ListAPIView):
    # 独自に拡張
    def list(self,request,pk):
        self.queryset = Comment.objects.order_by('-created_at').filter(question_id=pk).all()
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)

        return Response(serializer.data)


