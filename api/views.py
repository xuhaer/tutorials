from django.shortcuts import render

# Create your views here.
from api.models import Question, Choice
from api.serializers import QuestionSerializer, ChoiceSerializer
from django.contrib.auth.models import User
from rest_framework import permissions


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly

class QuestionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
