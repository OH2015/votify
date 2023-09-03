from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import VoteViewSet,CommentViewSet,QuestionViewSet,UserViewSet,UpdateContentViewSet,GoogleSocialAuthView

from rest_framework import routers

defaultRouter = routers.DefaultRouter()
defaultRouter.register('user',UserViewSet)
defaultRouter.register('vote',VoteViewSet)
defaultRouter.register('comment',CommentViewSet)
defaultRouter.register('question',QuestionViewSet)
defaultRouter.register('update_content',UpdateContentViewSet)

app_name = 'polls'

urlpatterns = [
    # 画面
    # トップ画面
    path('', views.IndexView.as_view(), name='index'),
    # 更新履歴
    path('update_history/', views.UpdateHistory, name='update_history'),
    # 構成図
    path('diagram/', views.Diagram, name='diagram'),
    # 質問作成
    path('create_question/', views.CreateQuestion.as_view() , name='create_question'),

    # 仮登録
    path('register', views.RegisterView.as_view(), name='register'),
    # 本登録
    path('register_complete/<str:token>/', views.RegisterCompleteView.as_view(), name='register_complete'),
    # ログイン
    path('login/',views.Login,name='login'),
    # ログアウト
    path("logout/",views.Logout,name="logout"),
    # 個人トップ画面
    path('<str:id>/account_top/', views.AccountTop.as_view(), name='account_top'),
    # 個人情報
    path('<str:id>/account_info/', views.AccountInfo.as_view(), name='account_info'),
    # 退会
    path('<str:id>/account_delete/', views.AccountDelete.as_view(), name='account_delete'),

    # API
    # api/vote/に各CRUDエンドポイントを作成
    path('api/',include(defaultRouter.urls)),
    # ログインチェック
    path('api/get_user_id/', views.get_user_id),
    # 投票済みリスト取得
    path('api/get_voted_list/', views.get_voted_list),
    # ログアウト
    path('api/logout/', views.doLogout),
    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)