from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime

from django.contrib.auth.models import User
from ..models import Question

import random, string

def randomname(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def create_question(question_text, days):
    """
    与えられた引数でQuestionのインスタンスを生成する(引数の日付は現在時刻との日付差、正が未来、負が過去)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    username = randomname(10)
    password = randomname(20)
    user = User.objects.create_user(username, username + '@sample.com', password)
    return Question.objects.create(question_text=question_text, pub_date=time,author=user)

class QuestionIndexViewTests(TestCase):
    # １件も質問が存在しない場合
    def test_no_questions(self):
        """
        質問が一つもなければ適切なメッセージが表示されること
        """
        # http://polls/index/
        response = self.client.get(reverse('polls:index'))
        # レスポンスステータスが200番であること
        self.assertEqual(response.status_code, 200)
        # No polls are available.のメッセージが表示されること
        self.assertContains(response, "No polls are available.")
        # リストオブジェクトが空であること
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # 過去の質問の場合
    def test_past_question(self):
        """
        過去の質問が表示されていること
        """
        # 30日前で作成
        question = create_question(question_text="Past question.", days=-30)
        # http://polls/index/
        response = self.client.get(reverse('polls:index'))
        # 作成した質問がレスポンスオブジェクトに帰ってきていること
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    # 未来の質問
    def test_future_question(self):
        """
        未来の質問が表示されていないこと
        """
        # 30日後で作成
        create_question(question_text="Future question.", days=30)
        # https://polls/index/
        response = self.client.get(reverse('polls:index'))
        # No polls are available.の文字が表示されること
        self.assertContains(response, "No polls are available.")
        # レスポンスcontextが空であること
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # 未来の質問と過去の質問
    def test_future_question_and_past_question(self):
        """
        未来の質問が非表示で過去の質問が表示されること
        """
        # 30日前で作成
        question = create_question(question_text="Past question.", days=-30)
        # 30日後で作成
        create_question(question_text="Future question.", days=30)
        # https://polls/index
        response = self.client.get(reverse('polls:index'))
        # コンテキストが過去の方だけになっていること
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    # 過去の質問二つ
    def test_two_past_questions(self):
        """
        過去の質問が二つとも表示されること
        """
        # 30日前
        question1 = create_question(question_text="Past question 1.", days=-30)
        # 5日前
        question2 = create_question(question_text="Past question 2.", days=-5)
        # https://polls/index/
        response = self.client.get(reverse('polls:index'))
        # 両方がコンテキストに含まれていること
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

# 詳細画面のテスト
class QuestionDetailViewTests(TestCase):
    # 未来の質問
    def test_future_question(self):
        """
        未来の質問の詳細画面が４０４エラーになること
        """
        # 5日後
        future_question = create_question(question_text='Future question.', days=5)
        # https://polls/index
        url = reverse('polls:detail', args=(future_question.id,))
        # レスポンス取得
        response = self.client.get(url)
        # ステータス404になること
        self.assertEqual(response.status_code, 404)

    # 過去の質問
    def test_past_question(self):
        """
        過去の質問の詳細ページに質問のテキストが含まれていること
        """
        # ５日前の質問
        past_question = create_question(question_text='Past Question.', days=-5)
        # https://polls/index
        url = reverse('polls:detail', args=(past_question.id,))
        # レスポンス取得
        response = self.client.get(url)
        # レスポンスに作成した質問のテキストが含まれていること
        self.assertContains(response, past_question.question_text)