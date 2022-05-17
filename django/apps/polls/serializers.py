from email.policy import default
from rest_framework import serializers
from .models import Question,Choice


class QuestionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Question

      fields = ('id','title', 'watched', 'author', 'created_at', 'updated_at')



class ChoiceSerializer(serializers.ModelSerializer):
   class Meta:
       model = Choice
       fields = ('id','question', 'choice_text', 'votes', 'created_at', 'updated_at')
