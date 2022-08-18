from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = "delete non-active users created before yesterday"

    def handle(self, *args, **options):
        yesterday = timezone.now() - timedelta(days=1)
        users = get_user_model().objects.filter(is_active=False, created_at__lt=yesterday).all()
        count = users.count()
        users.delete()
        print(f'{count}件のユーザーを削除しました')

