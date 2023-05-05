from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( PhoneQuestionSerializer, 
PhoneQuestionCREATESerializer, PhoneQuestionLISTSerializer, 
PhoneQuestionDETAILSerializer, PhoneQuestionUPDATESerializer)
from app.models import PhoneQuestion

import django_filters

class PhoneQuestionFilterSet(django_filters.FilterSet):
    class Meta:
        model = PhoneQuestion
        fields = ('id', 'title', 'date_created')

class PhoneQuestionViewSet(BaseActionsModelViewSet):
    queryset = PhoneQuestion.objects.all()
    serializer_class = PhoneQuestionSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = PhoneQuestionFilterSet

    action_serializers = {
        'create': PhoneQuestionCREATESerializer,
        'list': PhoneQuestionLISTSerializer,
        'retrieve': PhoneQuestionDETAILSerializer,
        'update': PhoneQuestionUPDATESerializer,
        'partial_update': PhoneQuestionUPDATESerializer
    }