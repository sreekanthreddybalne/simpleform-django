from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( SimpleFormSerializer, 
SimpleFormCREATESerializer, SimpleFormLISTSerializer, 
SimpleFormDETAILSerializer, SimpleFormUPDATESerializer)
from app.models import SimpleForm

import django_filters

class SimpleFormFilterSet(django_filters.FilterSet):
    class Meta:
        model = SimpleForm
        fields = ('id', 'is_published', 'date_created')

class SimpleFormViewSet(BaseActionsModelViewSet):
    queryset = SimpleForm.objects.all()
    serializer_class = SimpleFormSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'title', 'workspace__title', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = SimpleFormFilterSet

    action_serializers = {
        'create': SimpleFormCREATESerializer,
        'list': SimpleFormLISTSerializer,
        'retrieve': SimpleFormDETAILSerializer,
        'update': SimpleFormUPDATESerializer,
        'partial_update': SimpleFormUPDATESerializer
    }