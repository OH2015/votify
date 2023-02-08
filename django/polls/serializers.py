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


class QuestionSerializer(serializers.ModelSerializer):
   author = UserSerializer()
   choices = ChoiceSerializer(many=True,read_only=True)

   class Meta:
      model = Question

      fields = ('id','title','explanation','watched','author','genre','auth_level','created_at','choices')


class CommentSerializer(serializers.ModelSerializer):
   user = UserSerializer()

   class Meta:
      model = Comment
      fields = ('id','question', 'user', 'text', 'created_at', 'updated_at','get_date')

