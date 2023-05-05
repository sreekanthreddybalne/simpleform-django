from django.core.management.base import BaseCommand
from app.models import Role, User
from api.serializers import RoleCREATESerializer
import re
from rest_framework import serializers

from django.contrib.contenttypes.models import ContentType
from app.helpers import concrete_model_inheritors

class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, help='Define a username', )
        parser.add_argument('-p', '--password', type=str, help='Define a password', )

    def handle(self, *args, **kwargs):
        user = User.objects.get(uuid="AnonymousUser")

        #handle roles creation
        user_models = concrete_model_inheritors(User)
        for user_model in user_models:
            content_type = ContentType.objects.get(model=user_model.__name__.lower())
            q = Role.objects.filter(user_model = content_type)
            if q.exists():
                self.stdout.write(self.style.HTTP_NOT_MODIFIED('Role "%s" exists' % q[0].name))
            else:
                context = {
                    "user": user
                }
                data = {
                    "name": re.sub("([a-z])([A-Z])","\g<1> \g<2>",user_model.__name__),
                    "user_model": content_type.pk,
                }
                serializer = RoleCREATESerializer(data=data, context=context)
                if serializer.is_valid():
                    instance = serializer.save()
                    self.stdout.write(self.style.SUCCESS('Role "%s" created successfully' % instance.name))
                else:
                    self.stdout.write(self.style.ERROR(serializer.errors))
        self.stdout.write(self.style.SUCCESS('Project initiation done.'))
        return
