from rest_framework import serializers
from api.models import Question, Choice


class QuestionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        '''using the ModelSerializer class to refactor serializer '''
        model = Question
        fields = ('url', 'question_text', 'pub_date')


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Choice
        fields = ('url', 'question', 'choice_text', 'votes')
