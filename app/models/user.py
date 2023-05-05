
from django.db import models
from django.contrib.auth.models import AbstractUser
from .base import AppModel
from app.managers import UserManager

class User(AppModel, AbstractUser):
    email =  models.EmailField(max_length=70, unique=True)
    # email = None
    #password =  //This is a default field and required for us.
    #is_active = //This is a default field and required for us.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.username