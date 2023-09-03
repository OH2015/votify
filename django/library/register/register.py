from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = get_user_model().objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            new_user = get_user_model().objects.get(email=email)

            registered_user = get_user_model().objects.get(email=email)
            registered_user.check_password(settings.SOCIAL_SECRET)

            Token.objects.filter(user=registered_user).delete()
            Token.objects.create(user=registered_user)
            new_token = list(Token.objects.filter(
                user_id=registered_user).values("key"))

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'password': settings.SOCIAL_SECRET,
                'tokens': str(new_token[0]['key'])}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': email, 'email': email,
            'password': settings.SOCIAL_SECRET
        }
        user = get_user_model().objects.create_user(**user)
        user.is_active = True
        user.auth_provider = provider
        user.save()
        new_user = get_user_model().objects.get(email=email)
        new_user.check_password(settings.SOCIAL_SECRET)
        Token.objects.create(user=new_user)
        new_token = list(Token.objects.filter(user_id=new_user).values("key"))
        return {
            'email': new_user.email,
            'username': new_user.username,
            'password': settings.SOCIAL_SECRET,
            'tokens': str(new_token[0]['key']),
        }
