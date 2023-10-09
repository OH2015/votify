from .serializers import *
from .forms import UserForm
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import management
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView  # テンプレートタグ
from django.shortcuts import render
from django.template.loader import render_to_string


# アカウント登録
class RegisterView(TemplateView):
    def __init__(self):
        self.params = {"message": ''}

    # Get処理
    def get(self, request):
        return render(request, "polls/register.html", context=self.params)

    # Post処理
    def post(self, request):
        form = UserForm(request.POST)
        # 入力値のバリデーション
        if form.is_valid():
            # 期限切れのユーザを削除
            management.call_command('clean_users')
            # 重複確認
            if get_user_model().objects.filter(email=form.cleaned_data['email']).exists():
                self.params["message"] = 'このメールアドレスは既に使用されています。'
                return render(request, "polls/register.html", context=self.params)
            elif get_user_model().objects.filter(username=form.cleaned_data['username']).exists():
                self.params["message"] = 'このユーザー名は既に使用されています。'
                return render(request, "polls/register.html", context=self.params)
            # 重複がなければ登録
            else:
                user = get_user_model().objects.create_user(
                    username=form.cleaned_data['email'].split('@')[0],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    profile=form.cleaned_data['profile'])
                user.is_active = False
                user.save()

            # 本登録用のメール送信
            current_site = get_current_site(self.request)
            domain = current_site.domain
            context = {
                'protocol': self.request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
            }
            subject = render_to_string('polls/subject.txt', context)
            message = render_to_string('polls/message.txt', context)
            user.email_user(subject, message)

            return render(request, "polls/register_done.html", context=self.params)
        else:
            self.params["message"] = form.errors
            return render(request, "polls/register.html", context=self.params)


# 本登録画面
class RegisterCompleteView(TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'polls/register_complete.html'
    timeout_seconds = 60*60*24  # 一日で無効化

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            print('期限切れです')
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            print('トークンが間違っています')
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = get_user_model().objects.get(pk=user_pk)
            except get_user_model().DoesNotExist:
                print('ユーザーが存在しません')
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return render(request, "polls/register_complete.html")
