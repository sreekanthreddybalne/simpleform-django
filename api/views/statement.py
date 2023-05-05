from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( StatementSerializer, 
StatementCREATESerializer, StatementLISTSerializer, 
StatementDETAILSerializer, StatementUPDATESerializer)
from app.models import Statement

import django_filters

class StatementFilterSet(django_filters.FilterSet):
    class Meta:
        model = Statement
        fields = ('id', 'title', 'date_created')

class StatementViewSet(BaseActionsModelViewSet):
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = StatementFilterSet

    action_serializers = {
        'create': StatementCREATESerializer,
        'list': StatementLISTSerializer,
        'retrieve': StatementDETAILSerializer,
        'update': StatementUPDATESerializer,
        'partial_update': StatementUPDATESerializer
    }