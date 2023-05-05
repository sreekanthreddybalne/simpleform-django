from api.serializers.statement import StatementDETAILSerializer
from api.serializers.transition import TransitionDETAILSerializer
from api.serializers.choice_question import ChoiceQuestionDETAILSerializer
from api.serializers.phone_question import PhoneQuestionDETAILSerializer
from api.serializers.email_question import EmailQuestionDETAILSerializer
from api.serializers.text_question import TextQuestionDETAILSerializer
from api.serializers.common import CommonQuestionCREATEClass
from app.models.main import ChoiceQuestion, EmailQuestion, PhoneQuestion, Statement, TextQuestion
from rest_framework import serializers
import pyranker
from app.models import (BaseQuestion, )

class BaseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseQuestion
        fields = '__all__'

QUESTION_TYPES = {
    TextQuestion: TextQuestionDETAILSerializer,
    EmailQuestion: EmailQuestionDETAILSerializer,
    PhoneQuestion: PhoneQuestionDETAILSerializer,
    ChoiceQuestion: ChoiceQuestionDETAILSerializer,
    Statement: StatementDETAILSerializer
}

class BaseQuestionDETAILSerializer(serializers.ModelSerializer):
    child_transitions = TransitionDETAILSerializer(many=True)

    class Meta:
        fields = ("id", "title", "sub_title", "rank", "child_transitions")
        model = BaseQuestion

    def to_representation(self, instance, *args):
        for key in QUESTION_TYPES.keys():
            if hasattr(instance, key.__name__.lower()):
                instance = key.objects.get(pk=instance.id)
                return QUESTION_TYPES[key](instance=instance).data

class BaseQuestionLISTSerializer(BaseQuestionDETAILSerializer):
    pass

class BaseQuestionCREATESerializer(CommonQuestionCREATEClass):
    
    def to_representation(self, instance, *args):
        return BaseQuestionDETAILSerializer(instance=instance).data
        
class BaseQuestionUPDATESerializer(BaseQuestionCREATESerializer):
    
    def validate(self, attrs):
        attrs['simpleform'] = self.instance.simpleform
        attrs = super().validate(attrs)
        return attrs
