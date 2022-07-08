import math
from django.contrib.auth import get_user_model
from django.db import models
import datetime
from datetime import timedelta
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

# ジャンル
class Genre(models.Model):
    title = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# 質問
class Question(models.Model):
    title = models.CharField(max_length=20)
    explanation = models.TextField(max_length=200)
    watched = models.IntegerField(default=0)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE )
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# 選択肢
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text

# 票
class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return self.choice.choice_text + ' : ' + self.user.username
        else:
            return self.choice.choice_text + ' : Anonymous'

# コメント
class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    # 日付文字列取得
    def get_date(self):
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


# ユーザーアカウントのモデルクラス
class Account(models.Model):
    # Djangoのデフォルトユーザモデルと1v1で紐づく
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 追加フィールド
    # プロフィール文章
    profile = models.TextField(max_length=1000,default='')

    def __str__(self):
        return self.user.username