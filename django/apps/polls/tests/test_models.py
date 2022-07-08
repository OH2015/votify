import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User
from ..models import Question

def create_question(title, days):
    """
    与えられた引数でQuestionのインスタンスを生成する(引数の日付は現在時刻との日付差、正が未来、負が過去)
    """
    
    user = User.objects.create_user('test_user', 'test@sample.com', 'test_password')
    return Question.objects.create(title=title,author=user)


class QuestionModelTests(TestCase):
    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        question = create_question(title="", days=0)
        title = "test_auestion_text"
        question.title = title
        question.save()

        saved_questions = Question.objects.all()
        actual_question = saved_questions[0]

        self.assertEqual(actual_question.title, title)







