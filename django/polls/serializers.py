from rest_framework import serializers
from .models import Question,Choice,Comment, Vote
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = get_user_model()

      fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
   votes = serializers.SerializerMethodField()

   class Meta:
      model = Choice
      fields = ('id','question', 'choice_text', 'votes', 'created_at', 'updated_at')

   def get_votes(self, instance):
      return Vote.objects.filter(choice=instance).all().count()

class CommentSerializer(serializers.ModelSerializer):
   # 受信(GET)用
   user = UserSerializer(read_only=True)
   # 送信(POST)用
   user_id = serializers.IntegerField(write_only=True)

   class Meta:
      model = Comment
      fields = '__all__'

   # POST時にユーザIDからユーザオブジェクトを取得
   def create(self, validated_data):
      user_id = validated_data.pop('user_id')
      user = get_user_model().objects.get(id=user_id)
      comment = Comment.objects.create(user=user, **validated_data)
      return comment


class QuestionSerializer(serializers.ModelSerializer):
   author = UserSerializer()
   choices = ChoiceSerializer(many=True,read_only=True)
   comments = CommentSerializer(many=True,read_only=True)

   class Meta:
      model = Question

      fields = ('id','title','explanation','watched','author','genre','auth_level','created_at','choices','comments')

class VoteSerializer(serializers.ModelSerializer):
   class Meta:
      model = Vote
      fields = '__all__'

