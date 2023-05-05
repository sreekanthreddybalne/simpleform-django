from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( TransitionSerializer, 
TransitionCREATESerializer, TransitionLISTSerializer, 
TransitionDETAILSerializer, TransitionUPDATESerializer)
from app.models import Transition

import django_filters

class TransitionFilterSet(django_filters.FilterSet):
    class Meta:
        model = Transition
        fields = ('id', 'from_question', 'to_question', 'on_value', 'date_created')

class TransitionViewSet(BaseActionsModelViewSet):
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = TransitionFilterSet

    action_serializers = {
        'create': TransitionCREATESerializer,
        'list': TransitionLISTSerializer,
        'retrieve': TransitionDETAILSerializer,
        'update': TransitionUPDATESerializer,
        'partial_update': TransitionUPDATESerializer
    }