from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "create a guest user"

    def handle(self, *args, **options):
        try:
            User.objects.get(username='guest')
        except User.DoesNotExist:
            User.objects.create_user('guest', 'guest@sample.com', 'guest_pass123@')
            print("creating guest is succseeded.")
        else:
            print("guest is already exists.")

