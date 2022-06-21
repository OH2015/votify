from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .models import Account, Genre, Question,Choice,Vote,UpdateContent,Comment
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import TemplateView # テンプレートタグ
from rest_framework import generics
from .serializers import ChoiceSerializer, QuestionSerializer, CommentSerializer
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse



# トップ画面
class IndexView(TemplateView):
    # これを書かなかったらデフォルトで「polls/Question_list.html」が探される
    template_name = 'polls/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['genres'] = Genre.objects.all()
        return ctx


# 投票画面
class VoteView(TemplateView):
    # GET(pk:question_id)
    def get(self, request,pk):
        question = get_object_or_404(Question, pk=pk)
        # 閲覧回数をカウント
        question.watched += 1
        question.save()
        self.params = {'question': question,'voted_choice_id':-1}
        
        # ログイン中
        if request.user.is_authenticated:
            # 自分の投稿
            if request.user == question.author:
                return render(request,"polls/detail.html",self.params)
            # 投票済み
            elif Vote.objects.filter(user=request.user,question=question).exists():
                self.params['voted_choice_id'] = Vote.objects.get(question=question,user=request.user).choice.id
                return render(request,"polls/detail.html",self.params)
            # 未投票
            else:
                return render(request,"polls/vote.html",self.params)
        # 匿名
        else:
            # 投票済み
            if str(pk) in request.session:
                self.params['voted_choice_id'] = request.session[str(pk)]
                print(request.session[str(pk)])
                return render(request,"polls/detail.html",self.params)
            # 未投票
            else:
                return render(request,"polls/vote.html",self.params)

    # 投票処理
    def post(self,request,pk):
        question = get_object_or_404(Question, pk=pk)
        choice = Choice.objects.get(id=request.POST['choice'])

        # ログイン中
        if request.user.is_authenticated:
            # 自分の投稿
            if request.user == question.author:
                return redirect('polls:vote',pk)
            # 投票済み
            elif Vote.objects.filter(user=request.user,question=question).exists():
                return redirect('polls:vote',pk)
        # 匿名
        else:
            # 投票済み
            if str(pk) in request.session:
                return redirect('polls:vote',pk)

        # ログイン中
        if request.user.is_authenticated:
            Vote.objects.create(question=choice.question,choice=choice,user=request.user)
        # 匿名
        else:
            Vote.objects.create(question=choice.question,choice=choice,user=None)

        # セッションに投票済み登録
        request.session[str(choice.question.id)] = choice.id
        return redirect('polls:vote',pk)


# 再投票
class RevoteView(TemplateView):
    # GET(pk:question_id)
    def get(self, request,pk):
        vote = Vote.objects.get(user=request.user,question=pk)
        vote.delete()

        return redirect('polls:vote',pk)


# コメント投稿API
class PostComment(TemplateView):
    def post(self,request,pk):
        Comment.objects.create(question_id=pk,user=request.user,text=request.POST.get('text'))
        return JsonResponse({})

# 更新履歴
def UpdateHistory(request):
    return render(request,"polls/update_history.html",{"contents":UpdateContent.objects.all})

# 構成図
def Diagram(request):
    return render(request,"polls/diagram.html")

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

# アカウントトップ画面
class  AccountTop(TemplateView):
    # Get処理
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        account = get_object_or_404(Account, user=user)
        questions = Question.objects.order_by('updated_at').filter(author=user).all()
        return render(request,"polls/account_top.html",{'account':account,"questions":questions})

    # Post処理
    def post(self,request,username):
        user = get_object_or_404(User, username=username)        
        id = request.POST.get('id')
        question = Question.objects.get(id=id)
        question.delete()
        return redirect('polls:account_top',user.username)



# 個人情報参照画面
class  AccountInfo(TemplateView):
    # Get処理
    def get(self,request,username):
        user = get_object_or_404(User, username=username)
        account = get_object_or_404(Account, user=user)
        if request.user == user:
            return render(request, 'polls/account_info.html',context={"account":account})
        else:
            return render(request, 'accounts/login.html')

    # Post処理
    def post(self,request,username):
        user = get_object_or_404(User, username=username)
        account = get_object_or_404(Account, user=user)
        username = request.POST.get('username')
        email = request.POST.get('email')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        profile = request.POST.get('profile')
        if username:
            user.username = username
        if email:
            user.email = email
        if last_name:
            account.last_name = last_name
        if first_name:
            account.first_name = first_name
        if profile:
            account.profile = profile

        user.save()
        account.save()

        return render(request, 'polls/account_info.html',context={"account":account})

    


# 
# DRF
# 

# Questionオブジェクトのリストを返すAPIビュー
class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()

    # 独自に拡張
    def list(self,request):
        condition1 = Q()
        condition2 = Q()
        keyword = request.query_params.get('keyword')
        genre = request.query_params.get('genre')

        # キーワードがあれば絞り込み
        if keyword:
            condition1 = Q(title__contains=keyword)

        # ジャンルがあれば絞り込み
        if genre:
            condition2 = Q(genre=genre)

        self.queryset = Question.objects.filter(condition1 & condition2).all()
        serializer = QuestionSerializer(self.get_queryset(),many=True)
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


# Commentオブジェクトのリストを返すAPIビュー
class CommentListAPIView(generics.ListAPIView):
    # 独自に拡張
    def list(self,request,pk):
        self.queryset = Comment.objects.order_by('-created_at').filter(question_id=pk).all()
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)

        return Response(serializer.data)


