from rest_framework import serializers
from .models import Question, Choice, Comment, Vote, UpdateContent
from django.contrib.auth import get_user_model
from django.db.models import Count


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    voted = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = (
            "id",
            "question",
            "choice_text",
            "votes",
            "voted",
            "created_at",
            "updated_at",
        )

    def get_votes(self, instance):
        return Vote.objects.filter(choice=instance).all().count()

    def get_voted(self, instance):
        request = self.context.get("request", None)
        # ログイン時
        if request.user.id:
            # 投票のレコードがあるか確認する
            return Vote.objects.filter(choice=instance, user=request.user.id).exists()
        # 未ログイン時
        else:
            # セッションで投票済か確認する
            voted_list = request.session.get("voted_list", [])
            return any(item.get("choice") == instance.id for item in voted_list)


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
    votes = serializers.SerializerMethodField()

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
            "votes",
        )

    def get_votes(self, instance):
        return (
            Question.objects.annotate(
                vote_count=Count("choices__vote__id", distinct=True)
            )
            .get(pk=instance.pk)
            .vote_count
        )


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"


class UpdateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateContent

        fields = "__all__"
