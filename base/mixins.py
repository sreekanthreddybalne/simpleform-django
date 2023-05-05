from django.shortcuts import get_list_or_404, get_object_or_404
from app.models import User

class MultipleFieldChainLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object

class ViewContextMixin(object):

    def get_serializer_context(self):
        # data = super().get_serializer_context()
        data = {}
        user = self.request.user
        if user and not user.is_authenticated:
            user = User.objects.get(uuid="AnonymousUser")
        data['user'] = user
        data['view'] = self
        data['request'] = self.request
        return data

class SerializerCreatedByModifiedByMixin(object):

    def validate(self, attrs):
        if self.context["request"].method == "POST" and "created_by" in self.Meta.fields:
            attrs["created_by"] = self.context["user"]
        elif self.context["request"].method in ["PUT", "PATCH"] and "modified_by" in self.Meta.fields:
            attrs["modified_by"] = self.context["user"]
        return attrs
