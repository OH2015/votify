from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Account


class Command(BaseCommand):
    help = "create a guest user"

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='guest')
        except User.DoesNotExist:
            user = User.objects.create_user('guest', 'guest@sample.com', 'guest_pass123@')
            Account.objects.create(user=user,first_name='hello',last_name='world')
            print("creating guest is succseeded.")
        else:
            print("guest is already exists.")

