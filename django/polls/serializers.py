from rest_framework import serializers
from .models import Question, Choice, Comment, Vote, UpdateContent
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ("id", "question", "choice_text", "votes", "created_at", "updated_at")

    def get_votes(self, instance):
        return Vote.objects.filter(choice=instance).all().count()


class CommentSerializer(serializers.ModelSerializer):
    # 受信(GET)用
    user = UserSerializer(read_only=True)
    # 送信(POST)用
    user_id = serializers.IntegerField(write_only=True)
    # 表示日時
    disp_date = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_disp_date(self, instance):
        return instance.get_disp_date()


class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    choices = ChoiceSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Question

        fields = (
            "id",
            "title",
            "explanation",
            "watched",
            "author",
            "genre",
            "auth_level",
            "created_at",
            "choices",
            "comments",
        )


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"


class UpdateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateContent

        fields = "__all__"
