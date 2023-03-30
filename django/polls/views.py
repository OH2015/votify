import json
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Question, Choice, Vote, UpdateContent, Comment
from .forms import UserForm
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView  # テンプレートタグ
from rest_framework import generics, viewsets
from rest_framework.response import Response
from .serializers import QuestionSerializer, CommentSerializer, UserSerializer, VoteSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest, JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import management
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string


# トップ画面
class IndexView(TemplateView):
    template_name = 'polls/index.html'


# 更新履歴
def UpdateHistory(request):
    return render(request, "polls/update_history.html", {"contents": UpdateContent.objects.all})


# 構成図
def Diagram(request):
    return render(request, "polls/diagram.html")


# 投稿
class CreateQuestion(TemplateView):
    def get(self, request):
        return render(request, 'polls/create.html', {'genres': [g[0] for g in Question.genre.field.choices]})

    def post(self, request):
        # JSONデータ
        data = json.loads(request.body)
        # 質問作成
        question = Question.objects.create(
            title=data['title'], explanation=data['explanation'], genre=data['genre'], auth_level=data['auth_level'], author=get_user_model().get_guest_user())
        # 選択肢作成
        for choice in data['choices']:
            Choice.objects.create(choice_text=choice, question=question)

        print('質問を1件作成しました')

        return JsonResponse({'success': True, 'question_id': question.id})


# アカウント登録
class RegisterView(TemplateView):
    def __init__(self):
        self.params = {"message": ''}

    # Get処理
    def get(self, request):
        return render(request, "polls/register.html", context=self.params)

    # Post処理
    def post(self, request):
        form = UserForm(request.POST)
        # 入力値のバリデーション
        if form.is_valid():
            # 期限切れのユーザを削除
            management.call_command('clean_users')
            # 重複確認
            if get_user_model().objects.filter(email=form.cleaned_data['email']).exists():
                self.params["message"] = 'このメールアドレスは既に使用されています。'
                return render(request, "polls/register.html", context=self.params)
            elif get_user_model().objects.filter(username=form.cleaned_data['username']).exists():
                self.params["message"] = 'このユーザー名は既に使用されています。'
                return render(request, "polls/register.html", context=self.params)
            # 重複がなければ登録
            else:
                user = get_user_model().objects.create_user(
                    username=form.cleaned_data['email'].split('@')[0],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    profile=form.cleaned_data['profile'])
                user.is_active = False
                user.save()

            # 本登録用のメール送信
            current_site = get_current_site(self.request)
            domain = current_site.domain
            context = {
                'protocol': self.request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
            }
            subject = render_to_string('polls/subject.txt', context)
            message = render_to_string('polls/message.txt', context)
            user.email_user(subject, message)

            return render(request, "polls/register_done.html", context=self.params)
        else:
            self.params["message"] = form.errors
            return render(request, "polls/register.html", context=self.params)


# 本登録画面
class RegisterCompleteView(TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'polls/register_complete.html'
    timeout_seconds = 60*60*24  # 一日で無効化

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            print('期限切れです')
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            print('トークンが間違っています')
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = get_user_model().objects.get(pk=user_pk)
            except get_user_model().DoesNotExist:
                print('ユーザーが存在しません')
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return render(request, "polls/register_complete.html")


# アカウントトップ画面
class AccountTop(TemplateView):
    # Get処理
    def get(self, request, id):
        user = get_object_or_404(get_user_model(), id=id)
        questions = Question.objects.order_by(
            'updated_at').filter(author=user).all()
        return render(request, "polls/account_top.html", {"user": user, "questions": questions})

    # Post処理
    def post(self, request, id):
        user = get_object_or_404(get_user_model(), id=id)
        id = request.POST.get('id')
        # 質問の削除
        question = Question.objects.get(id=id)
        question.delete()
        return redirect('polls:account_top', user.id)


# 個人情報参照画面
class AccountInfo(TemplateView):
    # Get処理
    def get(self, request, id):
        user = get_object_or_404(get_user_model(), id=id)
        if request.user == user:
            return render(request, 'polls/account_info.html', context={"user": user})
        else:
            return render(request, 'polls/login.html')

    # Post処理
    def post(self, request, id):
        user = get_object_or_404(get_user_model(), id=id)
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile = request.POST.get('profile')
        if username:
            user.username = username
        if email:
            user.email = email
        if profile:
            user.profile = profile

        user.save()

        return render(request, 'polls/account_info.html', context={"user": user})


# 退会
class AccountDelete(TemplateView):
    # Get処理
    def get(self, request, id):
        user = get_object_or_404(get_user_model(), id=id)
        if user == request.user:
            user.delete()

        return redirect('polls:index')


# ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のメールアドレス・パスワード取得
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(request, email=email, password=password)

        # ユーザー認証
        if user:
            # ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponse("Login Success")
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'polls/login.html')


# ログアウト
@login_required
def Logout(request):
    logout(request)
    # トップ画面遷移
    return HttpResponseRedirect(reverse('polls:index'))


#
# DRF(DjangoRestFramework)
#

# ユーザーモデルのCRUDエンドポイント
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        # 更新する項目だけのリクエストを許可する
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


# 質問モデルのCRUDエンドポイント
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # GET処理のカスタマイズ
    def list(self, request):
        queryset = self.get_queryset()
        question_id = request.query_params.get('question_id')

        # IDがあれば絞り込み
        if question_id:
            queryset = queryset.filter(id=question_id)

        return Response(QuestionSerializer(queryset, many=True).data)


# 投票モデルのCRUDエンドポイント
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request):
        # TODO 後でリファクタ
        data = request.data
        # 重複チェック
        if request.user.is_authenticated:
            if Vote.objects.filter(user=request.user, question_id=data['question']).exists():
                Vote.objects.filter(user=request.user, question_id=data['question']).delete()

        user = request.user if request.user.is_authenticated else None
        vote = Vote.objects.create(
            question_id=data['question'], user=user, choice_id=data['choice'])
        data['vote'] = vote.id
        vote.save()
        # 未ログイン時はセッションに保存
        if not request.user.is_authenticated:
            voted_list = request.session.get('voted_list', [])
            new_voted_list = []
            for voted in voted_list:
                if voted['question'] == data['question']:
                    Vote.objects.get(id=voted['vote']).delete()
                else:
                    new_voted_list.append(voted)

            new_voted_list.append(data)
            request.session['voted_list'] = new_voted_list

        return Response({'id': vote.id})

    def destroy(self, request, pk=None):
        # TODO 後でリファクタ
        # 未ログイン時はセッションを削除
        if not request.user.is_authenticated:
            voted_list = request.session.get('voted_list', [])
            new_voted_list = []
            for voted in voted_list:
                if voted['vote'] != int(pk):
                    new_voted_list.append(voted)

            request.session['voted_list'] = new_voted_list

        return super().destroy(request)


# コメントモデルのCRUDエンドポイント
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('-created_at').all()
    serializer_class = CommentSerializer

    # GET
    def get_queryset(self):
        queryset = Comment.objects.order_by('-created_at').all()
        question_id = self.request.query_params.get('question_id', None)
        # /api/comment/?question_id=1などで検索可能にする
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        return queryset


# ログインチェック(API用)
def check_login(request):
    return JsonResponse({"logined": request.user.is_authenticated})


# TODO　後でリファクタ
def get_voted_list(request):
    if request.user.is_authenticated:
        voted_list = []
        votes = list(Vote.objects.filter(user=request.user).all().values())
        for vote in votes:
            voted_list.append(
                {"vote": vote['id'],
                 "question": vote['question_id'],
                 "choice": vote['choice_id']
                 })
    else:
        voted_list = request.session.get('voted_list', [])
    return JsonResponse(voted_list, safe=False)
