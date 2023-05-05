from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( TextQuestionSerializer, 
TextQuestionCREATESerializer, TextQuestionLISTSerializer, 
TextQuestionDETAILSerializer, TextQuestionUPDATESerializer)
from app.models import TextQuestion

import django_filters

class TextQuestionFilterSet(django_filters.FilterSet):
    class Meta:
        model = TextQuestion
        fields = ('id', 'title', 'date_created')

class TextQuestionViewSet(BaseActionsModelViewSet):
    queryset = TextQuestion.objects.all()
    serializer_class = TextQuestionSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = TextQuestionFilterSet

    action_serializers = {
        'create': TextQuestionCREATESerializer,
        'list': TextQuestionLISTSerializer,
        'retrieve': TextQuestionDETAILSerializer,
        'update': TextQuestionUPDATESerializer,
        'partial_update': TextQuestionUPDATESerializer
    }