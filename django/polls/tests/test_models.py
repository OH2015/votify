from django.test import TestCase
from ..models import Question
from django.contrib.auth import get_user_model


class QuestionModelTests(TestCase):
    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        user = get_user_model().objects.create(username='テスト',email='sample@sample.com',password='pass')
        question = Question.objects.create(author=user)
        title = "test_auestion_text"
        question.title = title
        question.save()

        saved_questions = Question.objects.all()
        actual_question = saved_questions[0]

        self.assertEqual(actual_question.title, title)







