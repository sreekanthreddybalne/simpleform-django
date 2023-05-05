from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( ChoiceQuestionSerializer, 
ChoiceQuestionCREATESerializer, ChoiceQuestionLISTSerializer, 
ChoiceQuestionDETAILSerializer, ChoiceQuestionUPDATESerializer)
from app.models import ChoiceQuestion

import django_filters

class ChoiceQuestionFilterSet(django_filters.FilterSet):
    class Meta:
        model = ChoiceQuestion
        fields = ('id', 'title', 'date_created')

class ChoiceQuestionViewSet(BaseActionsModelViewSet):
    queryset = ChoiceQuestion.objects.all()
    serializer_class = ChoiceQuestionSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = ChoiceQuestionFilterSet

    action_serializers = {
        'create': ChoiceQuestionCREATESerializer,
        'list': ChoiceQuestionLISTSerializer,
        'retrieve': ChoiceQuestionDETAILSerializer,
        'update': ChoiceQuestionUPDATESerializer,
        'partial_update': ChoiceQuestionUPDATESerializer
    }