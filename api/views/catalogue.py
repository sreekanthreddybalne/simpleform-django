from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( CatalogueSerializer, 
CatalogueCREATESerializer, CatalogueLISTSerializer, 
CatalogueDETAILSerializer, CatalogueUPDATESerializer)
from app.models import Catalogue

import django_filters

class CatalogueFilterSet(django_filters.FilterSet):
    class Meta:
        model = Catalogue
        fields = ('id', 'name', 'date_created')

class CatalogueViewSet(BaseActionsModelViewSet):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = CatalogueFilterSet

    action_serializers = {
        'create': CatalogueCREATESerializer,
        'list': CatalogueLISTSerializer,
        'retrieve': CatalogueDETAILSerializer,
        'update': CatalogueUPDATESerializer,
        'partial_update': CatalogueUPDATESerializer
    }