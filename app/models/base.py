from django.db import models
from app.managers import RandomManager

class AppModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = RandomManager()

    class Meta:
        abstract = True
