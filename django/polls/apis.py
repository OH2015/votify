import json
from .serializers import *
from .models import Question, Vote, UpdateContent, Comment
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


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
        request.session['hoge'] = 4
        # TODO 後でリファクタ
        data = request.data
        # 重複チェック
        if request.user.is_authenticated:
            if Vote.objects.filter(user=request.user, question_id=data['question']).exists():
                Vote.objects.filter(user=request.user,
                                    question_id=data['question']).delete()

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
            request.session['hoge'] = 2

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

# 更新内容モデルのCRUDエンドポイント


class UpdateContentViewSet(viewsets.ModelViewSet):
    queryset = UpdateContent.objects.all()
    serializer_class = UpdateContentSerializer


def doLogin(request):
    request_json = json.loads(request.body)
    email = request_json.get('email')
    password = request_json.get('password')

    user = authenticate(request, email=email, password=password)

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

# ログインチェック(API用)


def get_user_id(request):
    user_id = -1 if not request.user.is_authenticated else request.user.id
    return JsonResponse({"user_id": user_id})


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


# ログアウト
@login_required
def doLogout(request):
    logout(request)
    return JsonResponse({"result": True})


# Google認証用API
@permission_classes((AllowAny, ))
class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


# ユーザ情報取得
def getUserInfo(request):
    if not request.user.is_authenticated:
        return JsonResponse({"id": None})
    user = get_user_model().objects.get(id=request.user.id)
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile": user.profile})

# 質問作成


@csrf_exempt
def createQuestion(request):
    data = json.loads(request.body)
    # 質問作成
    question = Question.objects.create(
        title=data['title'], explanation=data['explanation'], genre=data['genre'], auth_level=data['auth_level'], author_id=data['user'])
    # 選択肢作成
    for choice in data['choices']:
        Choice.objects.create(choice_text=choice, question=question)

    return JsonResponse({'success': True, 'question_id': question.id})
