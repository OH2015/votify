from django.db import models
import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # 作成/更新日時
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # 作成/更新日時
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text


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