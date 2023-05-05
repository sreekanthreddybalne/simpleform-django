from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( BaseQuestionSerializer, 
BaseQuestionCREATESerializer, BaseQuestionLISTSerializer, 
BaseQuestionDETAILSerializer, BaseQuestionUPDATESerializer)
from app.models import BaseQuestion

import django_filters

class BaseQuestionFilterSet(django_filters.FilterSet):
    class Meta:
        model = BaseQuestion
        fields = ('id', 'simpleform', 'title', 'date_created')

class BaseQuestionViewSet(BaseActionsModelViewSet):
    queryset = BaseQuestion.objects.all()
    serializer_class = BaseQuestionSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = BaseQuestionFilterSet

    action_serializers = {
        'create': BaseQuestionCREATESerializer,
        'list': BaseQuestionLISTSerializer,
        'retrieve': BaseQuestionDETAILSerializer,
        'update': BaseQuestionUPDATESerializer,
        'partial_update': BaseQuestionUPDATESerializer
    }