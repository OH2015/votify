from django.test import TestCase
from django.urls import reverse, resolve
from ..views import IndexView, UpdateHistory

class TestUrls(TestCase):

  """index ページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_post_index_url(self):
    view = resolve('/')
    self.assertEqual(view.func.view_class, IndexView)

  """更新履歴ページへのリダイレクトをテスト"""
  def test_post_list_url(self):
    view = resolve('update_history')
    self.assertEqual(view.func, UpdateHistory)