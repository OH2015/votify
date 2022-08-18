from datetime import timedelta
from datetime import datetime
from django.test import TestCase
from django.core import management
from django.contrib.auth import get_user_model


class GuestTests(TestCase):
    def test_delete_guest_user(self):
        """ゲストユーザーが削除されているかテスト"""
        guest = get_user_model().get_guest_user()

        if guest is not None:
            guest.delete()

        self.assertEqual(guest, None)

    def test_creating_guest_user(self):
        """指定した情報でゲストユーザーが作成されているかテスト"""
        management.call_command('guest')
        guest = get_user_model().get_guest_user
        self.assertNotEqual(guest, None)


class CleanUsersTests(TestCase):
    def test_delete_expired_user(self):
        """期限切れユーザーが削除されているかテスト"""
        user = get_user_model().objects.create_user(username='test_name',
            email='test@email.com',is_active=False)
        user.created_at = datetime.now() - timedelta(days=2)
        user.save()
        management.call_command('clean_users')
       
        try:
            user = get_user_model().objects.get(username='test_name',
                email='test@email.com',is_active=False)
        except get_user_model().DoesNotExist:
            user = None

        self.assertEqual(user, None)

    def test_dont_delete_user(self):
        """期限内のユーザーが削除されていないことをテスト"""
        user = get_user_model().objects.create_user(username='test_name',
            email='test@email.com',is_active=False)
        user.created_at = datetime.now() - timedelta(days=0.5)
        user.save()
        management.call_command('clean_users')
       
        try:
            user = get_user_model().objects.get(username='test_name',
                email='test@email.com',is_active=False)
        except get_user_model().DoesNotExist:
            user = None

        self.assertNotEqual(user, None)







