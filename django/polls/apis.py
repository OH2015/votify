import json
import random
import string
from .serializers import *
from .models import Question, Vote, UpdateContent, Comment
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response


# ユーザーモデルのCRUDエンドポイント
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        # 更新する項目だけのリクエストを許可する
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)


# 質問モデルのCRUDエンドポイント
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # GET処理のカスタマイズ
    def list(self, request):
        queryset = self.get_queryset()
        question_id = request.query_params.get("question_id")

        # IDがあれば絞り込み
        if question_id:
            queryset = queryset.filter(id=question_id)

        return Response(QuestionSerializer(queryset, many=True).data)


# 投票モデルのCRUDエンドポイント
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request):
        request.session["hoge"] = 4
        # TODO 後でリファクタ
        data = request.data
        # 重複チェック
        if request.user.is_authenticated:
            if Vote.objects.filter(
                user=request.user, question_id=data["question"]
            ).exists():
                Vote.objects.filter(
                    user=request.user, question_id=data["question"]
                ).delete()

        user = request.user if request.user.is_authenticated else None
        vote = Vote.objects.create(
            question_id=data["question"], user=user, choice_id=data["choice"]
        )
        data["vote"] = vote.id
        vote.save()
        # 未ログイン時はセッションに保存
        if not request.user.is_authenticated:
            voted_list = request.session.get("voted_list", [])
            new_voted_list = []
            for voted in voted_list:
                if voted["question"] == data["question"]:
                    Vote.objects.get(id=voted["vote"]).delete()
                else:
                    new_voted_list.append(voted)

            new_voted_list.append(data)
            request.session["voted_list"] = new_voted_list
            request.session["hoge"] = 2

        return Response({"id": vote.id})

    def destroy(self, request, pk=None):
        # TODO 後でリファクタ
        # 未ログイン時はセッションを削除
        if not request.user.is_authenticated:
            voted_list = request.session.get("voted_list", [])
            new_voted_list = []
            for voted in voted_list:
                if voted["vote"] != int(pk):
                    new_voted_list.append(voted)

            request.session["voted_list"] = new_voted_list

        return super().destroy(request)


# コメントモデルのCRUDエンドポイント
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by("-created_at").all()
    serializer_class = CommentSerializer

    # GET
    def get_queryset(self):
        queryset = Comment.objects.order_by("-created_at").all()
        question_id = self.request.query_params.get("question_id", None)
        # /api/comment/?question_id=1などで検索可能にする
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        return queryset


# 更新内容モデルのCRUDエンドポイント
class UpdateContentViewSet(viewsets.ModelViewSet):
    queryset = UpdateContent.objects.all()
    serializer_class = UpdateContentSerializer


@csrf_exempt
def do_login(request):
    request_json = json.loads(request.body)
    email = request_json.get("email")
    password = request_json.get("password")

    user = authenticate(request, email=email, password=password)

    if user:
        # ユーザーアクティベート判定
        if user.is_active:
            # ログイン
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return JsonResponse({"result": True})
        else:
            # アカウント利用不可
            return JsonResponse({"result": False, "message": "アカウントが無効です。"})
    # ユーザー認証失敗
    else:
        return JsonResponse({"result": False, "message": "ログイン情報に誤りがあります。"})


# TODO　後でリファクタ
def get_voted_list(request):
    if request.user.is_authenticated:
        voted_list = []
        votes = list(Vote.objects.filter(user=request.user).all().values())
        for vote in votes:
            voted_list.append(
                {
                    "vote": vote["id"],
                    "question": vote["question_id"],
                    "choice": vote["choice_id"],
                }
            )
    else:
        voted_list = request.session.get("voted_list", [])
    return JsonResponse(voted_list, safe=False)


# ログアウト
@login_required
def do_logout(request):
    logout(request)
    return JsonResponse({"result": True})


# ユーザ情報取得
def get_user_info(request):
    if not request.user.is_authenticated:
        return JsonResponse({"id": None})
    user = get_user_model().objects.get(id=request.user.id)
    return JsonResponse(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profile": user.profile,
        }
    )


# 質問作成
@csrf_exempt
def create_question(request):
    data = json.loads(request.body)
    # 質問作成
    question = Question.objects.create(
        title=data["title"],
        explanation=data["explanation"],
        genre=data["genre"],
        auth_level=data["auth_level"],
        author_id=data["user"],
    )
    # 選択肢作成
    for choice in data["choices"]:
        Choice.objects.create(choice_text=choice, question=question)

    return JsonResponse({"success": True, "question_id": question.id})


# アカウント登録
@csrf_exempt
def account_register(request):
    data = json.loads(request.body)
    username = data["username"]
    email = data["email"]
    password = data["password"]

    if get_user_model().objects.filter(email=email, is_active=True).exists():
        return JsonResponse({"result": False, "message": "このメールアドレスは既に使用されています。"})
    if get_user_model().objects.filter(username=username).exclude(email=email).exists():
        return JsonResponse({"result": False, "message": "このユーザ名は既に使用されています。"})

    if get_user_model().objects.filter(email=email, is_active=False).exists():
        user = get_user_model().objects.get(email=email)
        user.username = username
    else:
        user = get_user_model().objects.create_user(
            username=username, email=email, password=password, is_active=False
        )

    user.save()

    # メール送信
    context = {
        "host": request.META["HTTP_REFERER"],
        "token": dumps(user.pk),
        "username": username,
    }
    subject = render_to_string("polls/register_subject.txt", context)
    message = render_to_string("polls/register_message.txt", context)
    try:
        send_mail(subject, message, None, [email], fail_silently=False)
    except:
        return JsonResponse({"result": False, "message": "メールの送信中にエラーが発生しました。"})

    return JsonResponse({"result": True})


# アカウント本登録
@csrf_exempt
def account_register_complete(request, **kwargs):
    data = json.loads(request.body)
    token = data.get("token")

    timeout_seconds = 60 * 60 * 24
    try:
        user_pk = loads(token, max_age=timeout_seconds)
    except SignatureExpired:
        return JsonResponse({"result": False, "message": "URL有効期限切れです。"})
    except BadSignature:
        return JsonResponse({"result": False, "message": "無効なトークンです。"})

    try:
        user = get_user_model().objects.get(pk=user_pk)
    except get_user_model().DoesNotExist:
        return JsonResponse({"result": False, "message": "ユーザーが取得できませんでした。"})

    user.is_active = True
    user.save()
    return JsonResponse({"result": True, "message": "アカウントの登録が完了しました。"})


# パスワード再設定メール送信
@csrf_exempt
def password_reset_mail(request):
    data = json.loads(request.body)
    email = data["email"]

    try:
        user = get_user_model().objects.get(email=email, is_active=True)
    except get_user_model().DoesNotExist:
        user = None

    if user == None:
        return JsonResponse({"result": False, "message": "登録されていないメールアドレスです。"})

    # メール送信
    context = {
        "host": request.META["HTTP_REFERER"],
        "token": dumps(user.pk),
    }
    subject = render_to_string("polls/password_subject.txt", context)
    message = render_to_string("polls/password_message.txt", context)

    try:
        send_mail(subject, message, None, [email], fail_silently=False)
    except:
        return JsonResponse({"result": False, "message": "メールの送信中にエラーが発生しました。"})

    return JsonResponse({"result": True})


# パスワード再設定
@csrf_exempt
def password_reset(request, **kwargs):
    data = json.loads(request.body)
    token = data.get("token")
    password = data.get("password")

    timeout_seconds = 60 * 60 * 24
    try:
        user_pk = loads(token, max_age=timeout_seconds)
    except SignatureExpired:
        return JsonResponse({"result": False, "message": "URL有効期限切れです。"})
    except BadSignature:
        return JsonResponse({"result": False, "message": "無効なトークンです。"})

    try:
        user = get_user_model().objects.get(pk=user_pk)
    except get_user_model().DoesNotExist:
        return JsonResponse({"result": False, "message": "ユーザーが取得できませんでした。"})

    user.set_password(password)
    user.save()
    return JsonResponse({"result": True, "message": "パスワードの再設定が完了しました。"})


# パスワード再設定メール送信
@csrf_exempt
def password_reset_mail(request):
    data = json.loads(request.body)
    email = data["email"]

    try:
        user = get_user_model().objects.get(email=email, is_active=True)
    except get_user_model().DoesNotExist:
        user = None

    if user == None:
        return JsonResponse({"result": False, "message": "登録されていないメールアドレスです。"})

    # メール送信
    context = {
        "host": request.META["HTTP_REFERER"],
        "token": dumps(user.pk),
    }
    subject = render_to_string("polls/password_subject.txt", context)
    message = render_to_string("polls/password_message.txt", context)

    try:
        send_mail(subject, message, None, [email], fail_silently=False)
    except:
        return JsonResponse({"result": False, "message": "メールの送信中にエラーが発生しました。"})

    return JsonResponse({"result": True})


# Googleログイン
@csrf_exempt
def google_login(request):
    data = json.loads(request.body)
    email = data.get("email")
    google_id = data.get("google_id")

    # すでにアカウントが存在する場合
    if get_user_model().objects.filter(email=email).exists():
        user = get_user_model().objects.get(email=email)
        user.set_password(google_id)
        user.save()
        user = authenticate(request, email=email, password=google_id)
    # アカウントが存在しない場合
    else:
        user = get_user_model().objects.create_user(
            username="".join(
                random.choices(string.ascii_letters + string.digits, k=10)
            ),
            email=email,
            password=google_id,
        )
        user.save()

    if user is None:
        return JsonResponse({"result": False, "message": "ログインに失敗しました。"})

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    return JsonResponse({"result": True})
