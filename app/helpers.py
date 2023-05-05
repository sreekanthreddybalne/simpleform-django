
from django.db.models import deletion

def inheritors(klass):
    subclasses = []
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.append(child)
                work.append(child)
    return subclasses

def concrete_model_inheritors(kclass):
    subclasses = inheritors(kclass)
    return [i for i in subclasses if not i._meta.abstract]


def delete_without_parent(obj):
    collector = deletion.Collector(using=obj._state.db)
    collector.add([obj])
    collector.delete()
    return True