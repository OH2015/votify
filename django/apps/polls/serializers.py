from dataclasses import field
from email.policy import default
from rest_framework import serializers
from .models import Question,Choice,Comment,Genre
from django.contrib.auth.models import User

class GenreSerializer(serializers.ModelSerializer):
   class Meta:
      model = Genre

      fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User

      fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
   genre = GenreSerializer()

   class Meta:
      model = Question

      fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
   class Meta:
       model = Choice
       fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
   user = UserSerializer()

   class Meta:
       model = Comment
       fields = ('id','question', 'user', 'text', 'created_at', 'updated_at')
