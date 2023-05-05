from rest_framework import viewsets, serializers, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .mixins import ViewContextMixin
from .filters import CustomFilterBackend, CustomSearchFilter

# Create your views here.

class BaseAPIView(ViewContextMixin, APIView):
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.serializer_class

    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data,
            context = self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response(True)
        else:
            raise serializers.ValidationError(serializer.errors)
            return Response(False)


class BaseActionsModelViewSet(ViewContextMixin, viewsets.ModelViewSet):
    filter_backends = (CustomFilterBackend, CustomSearchFilter, filters.OrderingFilter,)
    ordering = ('-date_created',)
    class Meta:
        abstract = True

    def paginate_queryset(self, queryset):
        no_page = self.request.query_params.get('no_page', None)
        if no_page:
            return None
        return super().paginate_queryset(queryset)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many, context=self.get_serializer_context())
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            if is_many:
                data={idx: er for idx, er in enumerate(serializer.errors)}
                raise serializers.ValidationError(data)
            else:
                raise serializers.ValidationError(serializer.errors)


    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(self.__class__, 'before_update') and callable(getattr(self.__class__, 'before_update')):
            self.before_update(request, instance, *args, **kwargs)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        if hasattr(self, 'admin_action_serializers') and self.request.user.is_superuser:
            if self.action in self.admin_action_serializers:
                return self.admin_action_serializers[self.action]

        if hasattr(self, 'self_action_serializers') and self.request.user and self.request.user.is_authenticated:
            if self.action in self.self_action_serializers:
                obj=self.get_object()
                if isinstance(obj, User):
                    if obj == self.request.user:
                        return self.self_action_serializers[self.action]

        #This code block is only specific to this project roles
        if hasattr(self, 'advisor_action_serializers') and hasattr(self.request.user, 'advisor'):
            if self.action in self.advisor_action_serializers:
                return self.advisor_action_serializers[self.action]
        #End of code block

        if hasattr(self, 'auth_action_serializers') and self.request.user.is_authenticated:
            if self.action in self.auth_action_serializers:
                return self.auth_action_serializers[self.action]

        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return self.serializer_class

    def get_permissions(self):
        print(self.request.user)
        assert self.permission_classes is not None, (
            "'%s' should either include a `permission_classes` attribute, "
            "or override the `get_permissions()` method."
            % self.__class__.__name__
        )
        if hasattr(self, 'action_permissions'):
            if self.action in self.action_permissions:
                return [permission() for permission in self.action_permissions[self.action]]
        return [permission() for permission in self.permission_classes]