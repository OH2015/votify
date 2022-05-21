from email.policy import default
from rest_framework import serializers
from .models import Question,Choice,Comment


class QuestionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Question

      fields = ('id','title', 'watched', 'author', 'created_at', 'updated_at')

class ChoiceSerializer(serializers.ModelSerializer):
   class Meta:
       model = Choice
       fields = ('id','question', 'choice_text', 'votes', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Comment
       fields = ('id','question', 'user', 'text', 'created_at', 'updated_at')
