from rest_framework import serializers
from .models import Question,Choice


class QuestionSerializer(serializers.ModelSerializer):
   class Meta:
        model = Question
        #新規フィールドをメソッドの戻り値で作るフィールド追加
        is_staff = serializers.SerializerMethodField()
        fields = ('question_text', 'pub_date', 'author', 'created_at', 'updated_at')
        #フィールド値を決定するメソッド    
        def is_staff(self):
            return True if self.author=='administrator' else False


#複数オブジェクト扱う場合でも、その単体オブジェクト用シリアライザーは必要
class ChoiceSerializer(serializers.ModelSerializer):
   class Meta:
       model = Choice
       fields = ('question', 'choice_text', 'votes', 'created_at', 'updated_at')


#child属性に単体オブジェクトのシリアライザーインスタンスを割り当て、完成
class ChoiceListSerializer(serializers.ListSerializer):

   child = ChoiceSerializer()  