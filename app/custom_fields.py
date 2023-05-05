from django.db import models
import re

class FK(models.ForeignKey):
    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        super().contribute_to_class(cls, name, private_only=False, **kwargs)
        self.remote_field.related_name = ("_".join(re.findall('[A-Z][^A-Z]*', cls.__name__))+"s").lower()

class OneToOneField(models.OneToOneField):
    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        super().contribute_to_class(cls, name, private_only=False, **kwargs)
        self.remote_field.related_name = ("_".join(re.findall('[A-Z][^A-Z]*', cls.__name__))).lower()
