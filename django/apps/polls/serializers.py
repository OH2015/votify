from rest_framework import serializers
from .models import Account, Question,Choice,Comment, Vote
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User

      fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
   class Meta:
      model = Account

      fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
   author = UserSerializer()

   class Meta:
      model = Question

      fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
   votes = serializers.SerializerMethodField()

   class Meta:
      model = Choice
      fields = ('id','question', 'choice_text', 'votes', 'created_at', 'updated_at')

   def get_votes(self, instance):
      return Vote.objects.filter(choice=instance).all().count()


class CommentSerializer(serializers.ModelSerializer):
   user = UserSerializer()

   class Meta:
      model = Comment
      fields = ('id','question', 'user', 'text', 'created_at', 'updated_at','get_date')

