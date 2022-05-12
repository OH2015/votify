from posixpath import split
from django.shortcuts import get_object_or_404, redirect, render
from .models import Account, Question,Choice,UpdateContent
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from .forms import ChoiceForm, QuestionForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import TemplateView # テンプレートタグ
from rest_framework import generics
from .models import Question
from .serializers import ChoiceSerializer, QuestionSerializer
from rest_framework.response import Response
from braces.views import CsrfExemptMixin


class IndexView(generic.ListView):
    # これを書かなかったらデフォルトで「polls/Question_list.html」が探される
    template_name = 'polls/index.html'
    # これも書かなかったらデフォルトでquestion_listという変数名でビューに渡される
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    # これを書かなかったらデフォルトで「polls/Question_detail.html」が探される
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



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
        return render(request,"polls/detail.html",{
            'question': question,
            'has_voted': has_voted,
        })


# 更新履歴
def UpdateHistory(request):
    contents = UpdateContent.objects.all
    return render(request,"polls/update_history.html",{"contents":contents})


# 更新履歴削除 JSON返却
def DeleteUpdateContent(request):
    # POST
    if request.method == "POST" and request.POST.get('id',None):
        id = request.POST.get('id',None)
        try:
            content = UpdateContent.objects.get(pk=id)
        except UpdateContent.DoesNotExist:
            content = None
        else:
            content.delete()
        
        data = {
            "category":"delete",
            "id": id,
        }

        return JsonResponse(data)

# 更新履歴編集 JSON返却
def EditUpdateContent(request):
    # POST
    if request.method == "POST" and request.POST.get('id',None):
        id = request.POST.get('id',None)
        # content_text = request.POST.get('content_text',None)
        is_completed = request.POST.get('is_completed',None)
        try:
            content = UpdateContent.objects.get(pk=id)
        except UpdateContent.DoesNotExist:
            content = None
        else:
            # content.content_text = content_text
            content.is_completed = True
            content.save()
        
        data = {
            "category":"edit",
            "id": id,
            "content_text": content.content_text,
            "is_completed":content.is_completed,
            "updated_at":content.updated_at,
        }

        return JsonResponse(data)

# 更新履歴作成 JSON返却
def CreateUpdateContent(request):
    # POST
    if request.method == "POST" and request.POST.get('content_text',None):
        # 登録
        content = UpdateContent.objects.create(content_text=request.POST.get('content_text',None))
        
        data = {
            "category":"create",
            "id": content.id,
            "content_text": content.content_text,
            "is_completed":content.is_completed,
            "updated_at":content.updated_at,
        }

        return JsonResponse(data)

# 質問作成
@login_required
def create_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.pub_date = timezone.now()
            question.save()
            return redirect('polls:detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'polls/create.html', {'form': form})


# 選択肢作成
@login_required
def create_choice(request,pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.author = request.user
            choice.save()
            question = choice.question
            return redirect('polls:detail', pk=question.pk)
    else:
        form = ChoiceForm(initial=dict(question=question))
    return render(request, 'polls/create.html', {'form': form})


# 質問編集
@login_required
def edit_question(request,pk):
    question = get_object_or_404(Question, pk=pk)
    
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.pub_date = timezone.now()
            question.save()
            return redirect('polls:detail', pk=question.id)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'polls/edit.html', {'form': form,'question':question})

# 選択肢編集
@login_required
def edit_choice(request,pk):
    choice = get_object_or_404(Choice, pk=pk)
    
    if request.method == "POST":
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.author = request.user
            choice.save()
            question = choice.question
            print("choiceの更新が完了しました")
            return redirect('polls:detail', pk=question.id)
    else:
        form = ChoiceForm(instance=choice)

    return render(request, 'polls/edit.html', {'form': form})


# アカウント登録
class  AccountRegistration(TemplateView):
    def __init__(self):
        self.params = {
            "message":"",
        }

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



# 
# API
# 


# Questionオブジェクトのリストを返すAPIビュー
class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()

    # 独自に拡張
    def list(self,request):
        keyword = request.query_params.get('keyword')

        if keyword:
            # キーワードがあれば絞り込み
            self.queryset = Question.objects.filter(question_text__contains=keyword).all()

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

        self.queryset = Choice.objects.filter(question_id=pk).all()
        queryset = self.get_queryset()
        serializer = ChoiceSerializer(queryset, many=True)

        return Response(serializer.data)


# 投票用APIビュー
class ChoiceUpdateAPIView(CsrfExemptMixin,generics.UpdateAPIView):
    authentication_classes = []
    def update(self,request, pk):
        # 選択肢の投票数カウント
        choice = Choice.objects.get(id=pk)
        choice.votes += 1
        choice.save()

        # セッションに投票済み登録
        request.session[str(choice.question.id)] = "voted"


        return Response(None)


