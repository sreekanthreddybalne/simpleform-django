from __future__ import absolute_import, unicode_literals
from .mailer import *
from .models import *
from base import choices
import functools
from django.core.cache import cache
from celery import shared_task
from celery.task import task
from celery.exceptions import SoftTimeLimitExceeded
import random




@shared_task
def task_send_activation_mail(user_id):
    pass#return send_activation_mail(user_id)

@shared_task
def task_send_welcome_mail(user_id):
    pass#return send_welcome_mail(user_id)

@shared_task
def task_send_confirmation_mail(user_id):
    pass#return send_confirmation_mail(user_id)

@shared_task
def task_send_transaction_mail(transaction_id):
    pass#return send_transaction_mail(transaction_id)

@shared_task
def action_after_new_user_save(user_id):
    from api.serializers import RoomCREATESerializer
    user = User.objects.get(pk=user_id)
    ousers = User.objects.filter(role__in=choices.CHAT_ALLOWED_ROLES).exclude(email="AnonymousUser").exclude(pk=user_id)
    for ou in ousers:
        room = Room.objects.create()
        room.users.add(user.pk, ou.pk)
        room.save()

@shared_task
def action_after_new_prospect_save(prospect_id):
    prospect = Prospect.objects.get(pk=prospect_id)
    data={"prospect":prospect, "type": choices.PROSPECT_ACTIVITY_TYPE_CREATED}
    ProspectActivity.objects.create(**data)

    # bot=User.objects.get(email="whitehathackersree@gmail.com")
    # Message.objects.create(
    #     sender=bot,
    #     receiver=user,
    #     content="Hey, "+str(user.first_name)+"! Welcome to the Team."
    # )
