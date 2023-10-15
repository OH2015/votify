from . import apis
from .apis import (
    VoteViewSet,
    CommentViewSet,
    QuestionViewSet,
    UserViewSet,
    UpdateContentViewSet,
)
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

defaultRouter = routers.DefaultRouter()
defaultRouter.register("user", UserViewSet)
defaultRouter.register("vote", VoteViewSet)
defaultRouter.register("comment", CommentViewSet)
defaultRouter.register("question", QuestionViewSet)
defaultRouter.register("update_content", UpdateContentViewSet)

app_name = "polls"

urlpatterns = [
    # ログイン
    path("api/login/", apis.do_login),
    # Googleログイン
    path("api/google_login/", apis.google_login),
    # ログアウト
    path("api/logout/", apis.do_logout),
    # アカウント仮登録
    path("api/account_register/", apis.account_register),
    # アカウント本登録
    path("api/account_register_complete/", apis.account_register_complete),
    # パスワード再設定メール送信
    path("api/password_reset_mail/", apis.password_reset_mail),
    # パスワード再設定
    path("api/password_reset/", apis.password_reset),
    # api/に各CRUDエンドポイントを作成
    path("api/", include(defaultRouter.urls)),
    # ユーザ情報取得
    path("api/get_user_info/", apis.get_user_info),
    # 投票済みリスト取得
    path("api/get_voted_list/", apis.get_voted_list),
    # 質問作成
    path("api/create_question/", apis.create_question),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
