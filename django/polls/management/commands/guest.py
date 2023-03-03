from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from config.consts import GUEST_EMAIL, GUEST_NAME, GUEST_PR, GUEST_PW


class Command(BaseCommand):
    help = "create a guest user"

    def handle(self, *args, **options):
        try:
            get_user_model().objects.get(username='ゲスト')
        except get_user_model().DoesNotExist:
            get_user_model().objects.create_user(
                id=0,
                username=GUEST_NAME,
                email=GUEST_EMAIL,
                password=GUEST_PW,
                profile=GUEST_PR)
            print("creating guest is succseeded.")
        else:
            print("guest is already exists.")

