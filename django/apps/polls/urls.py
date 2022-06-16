from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'polls'

urlpatterns = [
    # 画面
    # トップ画面
    path('', views.IndexView.as_view(), name='index'),
    # 投票画面
    path('vote/<int:pk>/', views.VoteView.as_view(), name='vote'),
    # 再投票
    path('revote/<int:pk>/', views.RevoteView.as_view(), name='revote'),
    # 更新履歴
    path('update_history/', views.UpdateHistory, name='update_history'),
    # 質問作成
    path('create_question/', views.CreateQuestion.as_view() , name='create_question'),
    # コメント投稿
    path('post_comment/<int:pk>/', views.PostComment.as_view() , name='post_comment'),

    # 新規登録
    path('register', views.AccountRegistration.as_view(), name='register'),
    # 個人トップ画面
    path('<str:username>/account_top/', views.AccountTop.as_view(), name='account_top'),
    # 個人情報
    path('<str:username>/account_info', views.AccountInfo.as_view(), name='account_info'),

    # API
    path('api/questions/', views.QuestionListAPIView.as_view()),
    path('api/questions/<int:pk>/', views.QuestionRetrieveAPIView.as_view()),
    path('api/choices/<int:pk>/', views.ChoiceListAPIView.as_view()),
    path('api/comments/<int:pk>/', views.CommentListAPIView.as_view()),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)