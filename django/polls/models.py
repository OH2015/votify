import math
from django.contrib.auth import get_user_model
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from config.consts import GUEST_NAME


# カスタムユーザーモデル
class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"), max_length=50, validators=[username_validator], blank=True
    )
    email = models.EmailField(_("email_address"), unique=True)
    profile = models.TextField(max_length=200, default="")
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 認証方法(email,google)
    auth_provider = models.CharField(max_length=50, blank=True, default="email")

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_guest_user():
        try:
            guest = get_user_model().objects.get(username=GUEST_NAME)
        except get_user_model().DoesNotExist:
            guest = None
        return guest


# 質問
class Question(models.Model):
    title = models.CharField(max_length=20)
    explanation = models.TextField(max_length=200)
    watched = models.IntegerField(default=0)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    genre = models.CharField(
        choices=[
            ("学問", "学問"),
            ("ニュース", "ニュース"),
            ("SNS", "SNS"),
            ("娯楽", "娯楽"),
            ("ライフワーク", "ライフワーク"),
            ("その他", "その他"),
        ],
        max_length=10,
        default=("その他", "その他"),
    )
    # 認証レベル(0:ログイン不要,1:ログイン必要,2:マイナンバー連携必要)
    auth_level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# 選択肢
class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text


# 票
class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return self.choice.choice_text + " : " + self.user.username
        else:
            return self.choice.choice_text + " : Anonymous"


# コメント
class Comment(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    # 日付文字列取得
    def get_disp_date(self):
        delta = timezone.now() - self.created_at
        if delta.days < 1:
            if delta.seconds < 3600:
                return str(math.floor(delta / timedelta(minutes=1))) + "分前"
            else:
                return str(math.floor(delta / timedelta(hours=1))) + "時間前"
        elif delta.days < 30:
            return str(delta.days) + "日前"
        elif delta.days < 365:
            return str(math.floor(delta.days / 30)) + "ヶ月前"
        else:
            return str(math.floor(delta / timedelta(years=1))) + "年前"


# 更新内容
class UpdateContent(models.Model):
    # 更新内容
    content_text = models.CharField(max_length=200)
    # 完了フラグ
    is_completed = models.BooleanField(default=False)
    # 作成/更新日時
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content_text
