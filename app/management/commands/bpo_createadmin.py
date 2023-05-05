from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import User, Admin

class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('-e', '--email', type=str, help='Define an email', )
        parser.add_argument('-p', '--password', type=str, help='Define a password', )
        parser.add_argument('-u', '--username', type=str, help='Define a username', )

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        username = kwargs['username']
        errors = []
        if not email:
            errors.append("email is required. `-e` or `--email`")
        if not password:
            errors.append("password is required. `-p` or `--password`")
        if not username:
            errors.append("username is required. `-u` or `--username`")
        if email and User.objects.filter(email=email).exists():
            errors.append("A user with email %s already exists." % email)
        if username and User.objects.filter(username=username).exists():
            errors.append("A user with username %s already exists." % username)
        if len(errors) >0:
            print('\033[31m', "ERROR", '\033[0m', sep='')
            self.stdout.write("%s" % "\n".join(errors))
            return
        else:
            user = Admin.objects.create(email=email, username=username, is_superuser=True, is_active=True)
            user.set_password(password)
            user.save()
            print("Admin with username %s created successfully." % username)
            return
