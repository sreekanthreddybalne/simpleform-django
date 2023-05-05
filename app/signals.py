from app.models.main import BaseQuestion
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import pre_save, post_save
from app.models import User
from app.helpers import concrete_model_inheritors

@receiver(post_save, sender=User)
def after_user_save(sender, instance, created, **kwargs):
    if created:
        pass
        # transaction.on_commit(action_after_new_user_save.s(instance.pk).delay)

# connect all subclasses of base content item too
for subclass in concrete_model_inheritors(User):
    post_save.connect(after_user_save, subclass)
