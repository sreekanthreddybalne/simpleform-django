from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( EmailQuestionSerializer, 
EmailQuestionCREATESerializer, EmailQuestionLISTSerializer, 
EmailQuestionDETAILSerializer, EmailQuestionUPDATESerializer)
from app.models import EmailQuestion

import django_filters

class EmailQuestionFilterSet(django_filters.FilterSet):
    class Meta:
        model = EmailQuestion
        fields = ('id', 'title', 'date_created')

class EmailQuestionViewSet(BaseActionsModelViewSet):
    queryset = EmailQuestion.objects.all()
    serializer_class = EmailQuestionSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = EmailQuestionFilterSet

    action_serializers = {
        'create': EmailQuestionCREATESerializer,
        'list': EmailQuestionLISTSerializer,
        'retrieve': EmailQuestionDETAILSerializer,
        'update': EmailQuestionUPDATESerializer,
        'partial_update': EmailQuestionUPDATESerializer
    }