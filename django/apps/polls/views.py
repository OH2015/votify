from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.urls import reverse
from .models import Account, Question,Choice,Vote,UpdateContent,Comment
from django.shortcuts import render
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.models import User
from django.views.generic import TemplateView # テンプレートタグ
from rest_framework import generics
from .serializers import ChoiceSerializer, QuestionSerializer, CommentSerializer
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required



# トップ画面
class IndexView(TemplateView):
    # これを書かなかったらデフォルトで「polls/Question_list.html」が探される
    template_name = 'polls/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['genres'] = [g[0] for g in Question.genre.field.choices]
        return ctx


# 投票画面
class VoteView(TemplateView):
    # GET(pk:question_id)
    def get(self, request,pk):
        question = get_object_or_404(Question, pk=pk)
        # 閲覧回数をカウント
        question.watched += 1
        question.save()
        auth_texts = ['匿名可','要ログイン','マイナンバー連携者限定']
        self.params = {
            'question': question
            ,'voted_choice_id':-1
            ,'auth_text': auth_texts[question.auth_level]}
        
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
                # 未投票 → 投票ページへ
                return render(request,"polls/vote.html",self.params)
        # 匿名
        else:
            # 投票済み
            if str(pk) in request.session:
                self.params['voted_choice_id'] = request.session[str(pk)]
                # 投票済み → 結果画面へ
                return render(request,"polls/detail.html",self.params)
            # 未投票
            else:
                # 投票権なし → 結果画面へ
                if question.auth_level > 0:
                    return render(request,"polls/detail.html",self.params)

                # 投票権あり → 投票ページへ
                else:
                    return render(request,"polls/vote.html",self.params)

    # 投票処理
    def post(self,request,pk):
        question = get_object_or_404(Question, pk=pk)
        choice = Choice.objects.get(id=request.POST['choice'])

        # ログイン中
        if request.user.is_authenticated:
            # 自分の投稿, 投票済み
            if request.user == question.author or Vote.objects.filter(user=request.user,question=question).exists():
                return redirect('polls:vote',pk)
        # 匿名
        else:
            # 投票済み, 投票権なし
            if str(pk) in request.session or question.auth_level > 0:
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
        return render(request, 'polls/create.html', {'genres':[g[0] for g in Question.genre.field.choices]})

    def post(self,request):
        # 選択肢の数
        choice_num = int(request.POST['choice_num'])
        print(request.POST['genre'])
            
        # 質問作成
        question = Question.objects.create(
            title=request.POST['question_title']
            ,explanation=request.POST['explanation']
            ,genre=request.POST['genre']
            ,auth_level=request.POST['auth_level']
            ,author=request.user)

        # 選択肢作成
        for i in range(choice_num):
            Choice.objects.create(choice_text=request.POST[f'choice{i}'],question=question)

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

        # ユーザ名重複チェック
        if User.objects.filter(username=id).exists():
            self.params["message"] = "そのユーザ名は既に登録されています。"
            return render(request,"polls/register.html",context=self.params)

        # メールアドレス重複チェック
        if User.objects.filter(email=email).exists():
            self.params["message"] = "そのメールアドレスは既に登録されています。"
            return render(request,"polls/register.html",context=self.params)
        
        try:
            user = User.objects.create_user(id,email,pw)
            Account.objects.create(user=user)
        except:
            if User.objects.filter(username=id).exists():
                User.objects.get(username=id).delete()
            self.params["message"] = "ユーザの作成に失敗しました"
            return render(request,"polls/register.html",context=self.params)

        self.params["message"] = "アカウントを作成しました"
        self.params["questions"] = Question.objects.order_by('updated_at').filter(author=user).all()
        self.params["account"] = Account.objects.get(user=user)

        # ログイン
        login(request,user)

        return render(request,"polls/account_top.html",context=self.params)

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
            return render(request, 'polls/login.html')

    # Post処理
    def post(self,request,username):
        user = get_object_or_404(User, username=username)
        account = get_object_or_404(Account, user=user)
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile = request.POST.get('profile')
        if username:
            user.username = username
        if email:
            user.email = email
        if profile:
            account.profile = profile

        user.save()
        account.save()

        return render(request, 'polls/account_info.html',context={"account":account})


#ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                return redirect('polls:index')
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'polls/login.html')


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('polls:login'))

# ゲストログイン
def guest_login(request):
    try:
        guest_user = User.objects.get(username='guest')
    except User.DoesNotExist:
        print("failes to login as guest")
    else:
        login(request, guest_user)
    return redirect('polls:index')
    


# 
# DRF(DjangoRestFramework)
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
        serializer = CommentSerializer(self.queryset, many=True)

        return Response(serializer.data)


