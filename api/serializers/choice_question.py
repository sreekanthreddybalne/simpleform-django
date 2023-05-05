from api.serializers.constants import Q_MULTIPLE_CHOICE
from api.serializers.common import CommonQuestionCREATEClass
from rest_framework import serializers
from app.models import (ChoiceQuestion, )
from .transition import TransitionDETAILSerializer
from .utils import add_all_transition

class ChoiceQuestionSerializer(serializers.ModelSerializer):
    qtype = serializers.ReadOnlyField(default=Q_MULTIPLE_CHOICE)
    child_transitions = TransitionDETAILSerializer(many=True)

    class Meta:
        model = ChoiceQuestion
        fields = ('id', 'simpleform', 'qtype', 'title', 'sub_title', 'rank', 'choices', 'child_transitions', 'date_created', 'date_modified')

class ChoiceQuestionLISTSerializer(ChoiceQuestionSerializer):
    pass

class ChoiceQuestionDETAILSerializer(ChoiceQuestionSerializer):
    pass

class ChoiceQuestionCREATESerializer(ChoiceQuestionSerializer, CommonQuestionCREATEClass):
    class Meta(CommonQuestionCREATEClass.Meta):
        model = ChoiceQuestion

    def to_representation(self, instance, *args):
        return ChoiceQuestionDETAILSerializer(instance=instance).data

    def create(self, validated_data):
        instance = super().create(validated_data)
        add_all_transition(instance.id)
        return instance

class ChoiceQuestionUPDATESerializer(ChoiceQuestionSerializer):

    class Meta:
        model = ChoiceQuestion
        fields = ('id', 'qtype', 'title', 'sub_title', 'rank', 'choices')
