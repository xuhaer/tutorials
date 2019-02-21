
# Create your views here.

from rest_framework import viewsets
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from api.serializers import QuestionSerializer, ChoiceSerializer

from polls.models import Question, Choice


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
