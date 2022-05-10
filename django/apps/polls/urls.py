from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'polls'

urlpatterns = [
    # 画面
    # トップ画面
    path('', views.IndexView.as_view(), name='index'),
    # 質問編集
    path('edit_question/<int:pk>/', views.edit_question, name='edit_question'),
    # 選択肢編集
    path('edit_choice/<int:pk>/', views.edit_choice, name='edit_choice'),
    # 詳細画面
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # 結果画面
    path('results/<int:pk>/', views.ResultsView.as_view(), name='results'),
    # 投票画面
    path('vote/<int:pk>/', views.Vote.as_view(), name='vote'),
    # 更新履歴トップ
    path('update_history/', views.UpdateHistory, name='update_history'),
    # 更新履歴作成
    path('update_history/create', views.CreateUpdateContent, name='update_content_create'),
    # 更新履歴削除
    path('update_history/delete', views.DeleteUpdateContent, name='update_content_delete'),
    # 更新履歴編集
    path('update_history/edit', views.EditUpdateContent, name='update_content_edit'),
    # 質問作成
    path('create_question/', views.create_question, name='create_question'),
    # 選択肢作成
    path('create_choice/<int:pk>/', views.create_choice, name='create_choice'),
    # 新規登録
    path('register', views.AccountRegistration.as_view(), name='register'),
    # マイページ
    path('mypage', views.mypage, name='mypage'),

    # API
    path('api/questions/', views.QuestionListAPIView.as_view()),
    path('api/questions/<int:pk>/', views.QuestionRetrieveAPIView.as_view()),
    path('api/choices/<int:pk>/', views.ChoiceListAPIView.as_view()),
    path('api/choices_update/<int:pk>/', views.ChoiceUpdateAPIView.as_view()),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)