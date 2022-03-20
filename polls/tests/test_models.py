import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from ..models import Question

class QuestionModelTests(TestCase):
    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        question = Question()
        question_text = "test_auestion_text"
        pub_date = timezone.now()
        question.question_text = question_text
        question.pub_date = pub_date
        question.save()

        saved_questions = Question.objects.all()
        actual_question = saved_questions[0]

        self.assertEqual(actual_question.question_text, question_text)
        self.assertEqual(actual_question.pub_date, pub_date)

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recentlyが未来の日付に対してFalseを返すこと
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recentlyが１日より前の日付に対してFalseを返すこと
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recentlyが１日以内の日付に対してTrueを返すこと
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)



