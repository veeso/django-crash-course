# Import serializers from REST framework
from rest_framework import serializers
# Import our models
from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_text', 'votes', 'id')

class QuestionBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text', 'pub_date', 'id')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    # Add choices to relations and serialize it using the `ChoiceSerializer`
    choices = ChoiceSerializer(many=True)
    class Meta:
        model = Question
        fields = ('question_text', 'pub_date', 'choices', 'id')
