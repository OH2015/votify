from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'polls'

urlpatterns = [
    # 画面
    # トップ画面
    path('', views.IndexView.as_view(), name='index'),
    # 結果画面
    path('results/<int:pk>/', views.ResultView.as_view(), name='results'),
    # 投票画面
    path('vote/<int:pk>/', views.Vote.as_view(), name='vote'),
    # 更新履歴
    path('update_history/', views.UpdateHistory, name='update_history'),

    # 質問作成
    path('create_question/', views.CreateQuestion.as_view() , name='create_question'),
    # 質問一覧
    path('my_questions/', views.MyQuestions.as_view() , name='my_questions'),
    # # 質問編集
    # path('edit_question/<int:pk>/', views.edit_question, name='edit_question'),

    # 新規登録
    path('register', views.AccountRegistration.as_view(), name='register'),
    # マイページ
    path('mypage', views.mypage, name='mypage'),

    # API
    path('api/questions/', views.QuestionListAPIView.as_view()),
    path('api/questions/<int:pk>/', views.QuestionRetrieveAPIView.as_view()),
    path('api/choices/<int:pk>/', views.ChoiceListAPIView.as_view()),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)