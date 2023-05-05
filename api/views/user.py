from rest_framework import permissions
from .base import BaseActionsModelViewSet
from api.utils import CustomPagination
from api.serializers import ( UserSerializer, 
UserCREATESerializer, UserLISTSerializer, 
UserDETAILSerializer, UserUPDATESerializer)
from app.models import User

import django_filters

class UserFilterSet(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ('id', 'username', 'date_created')

class UserViewSet(BaseActionsModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    search_fields = ('id', 'date_created')
    ordering_fields = ('id', 'date_created')
    filterset_class = UserFilterSet

    action_serializers = {
        'create': UserCREATESerializer,
        'list': UserLISTSerializer,
        'retrieve': UserDETAILSerializer,
        'update': UserUPDATESerializer,
        'partial_update': UserUPDATESerializer
    }