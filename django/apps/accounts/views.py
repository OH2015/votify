from django.shortcuts import redirect, render

# Create your views here
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy,reverse
from django.views import generic

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# 登録
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:Login')
    template_name = 'accounts/signup.html'

#ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                return redirect('polls:index')
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'accounts/login.html')


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('accounts:Login'))

# ゲストログイン
def guest_login(request):
    try:
        guest_user = User.objects.get(username='guest')
    except User.DoesNotExist:
        print("failes to login as guest")
    else:
        login(request, guest_user)
    return redirect('polls:index')