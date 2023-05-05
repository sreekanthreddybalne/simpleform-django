from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( WorkspaceSerializer, 
WorkspaceCREATESerializer, WorkspaceLISTSerializer, 
WorkspaceDETAILSerializer, WorkspaceUPDATESerializer)
from app.models import Workspace

import django_filters

class WorkspaceFilterSet(django_filters.FilterSet):
    class Meta:
        model = Workspace
        fields = ('id', 'date_created')

class WorkspaceViewSet(BaseActionsModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = WorkspaceFilterSet

    action_serializers = {
        'create': WorkspaceCREATESerializer,
        'list': WorkspaceLISTSerializer,
        'retrieve': WorkspaceDETAILSerializer,
        'update': WorkspaceUPDATESerializer,
        'partial_update': WorkspaceUPDATESerializer
    }