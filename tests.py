import datetime
from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    # １件も質問が存在しない場合
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
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
        Questions with a pub_date in the past are displayed on the
        index page.
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
        Questions with a pub_date in the future aren't displayed on
        the index page.
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
        Even if both past and future questions exist, only past questions
        are displayed.
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
        The questions index page may display multiple questions.
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
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
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
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        # ５日前の質問
        past_question = create_question(question_text='Past Question.', days=-5)
        # https://polls/index
        url = reverse('polls:detail', args=(past_question.id,))
        # レスポンス取得
        response = self.client.get(url)
        # レスポンスに作成した質問のテキストが含まれていること
        self.assertContains(response, past_question.question_text)