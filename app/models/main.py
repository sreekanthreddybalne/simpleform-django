from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
import json
from .base import AppModel
from .constants import (TEXT_QUESTION_TYPE_SHORT, TEXT_QUESTION_TYPES)

class BaseQuestion(AppModel):
    simpleform = models.ForeignKey(
        "SimpleForm",
        related_name="questions",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, default=None, blank=True, null=True)
    sub_title = models.CharField(max_length=255, default=None, blank=True, null=True)
    rank = models.CharField(max_length=255) # if they have the same rank, sort by id
    is_required = models.BooleanField(default=True)

    class Meta:
        unique_together = ('simpleform', 'rank',)

    def __str__(self):
        return self.title or ""

class Transition(AppModel):
    from_question = models.ForeignKey(
        "BaseQuestion",
        related_name="child_transitions",
        on_delete=models.CASCADE
    )
    on_value = models.CharField(max_length=255)
    to_question = models.ForeignKey(
        "BaseQuestion",
        related_name="parent_transitions",
        default=None,
        null=True, 
        blank=True,
        on_delete=models.CASCADE
    )
    is_end = models.BooleanField(default=False)

    def __str__(self):
        return self.from_question

class Statement(BaseQuestion):
    pass

class EmailQuestion(BaseQuestion):
    pass

class TextQuestion(BaseQuestion):
    placeholder = models.CharField(max_length=255, default=None, blank=True, null=True)
    text_type = models.PositiveSmallIntegerField(choices=TEXT_QUESTION_TYPES, default=TEXT_QUESTION_TYPE_SHORT)

class PhoneQuestion(BaseQuestion):
    pass

# default choice for choice question
def defaultChoice():
    return ["choice A"]

class ChoiceQuestion(BaseQuestion):
    """
    This question will have only two values
    """
    choices = ArrayField(models.CharField(max_length=255, default="", blank=True, null=True), default=defaultChoice)

class Response(AppModel):
    simpleform = models.ForeignKey(
        "SimpleForm",
        related_name="responses",
        on_delete=models.CASCADE
    )

class Answer(AppModel):
    response = models.ForeignKey(
        "Response",
        related_name="answers",
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        "BaseQuestion",
        related_name="answers",
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.question

class SimpleForm(AppModel):
    # if the workspace is null, assume it as a user workspace
    workspace = models.ForeignKey(
        "Workspace",
        related_name="simpleforms",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255) 
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Workspace(AppModel):
    title = models.CharField(max_length=255) #pesticide, fertilizer, seed

    def __str__(self):
        return self.title

class Briefing(AppModel):
    description = models.TextField()
    