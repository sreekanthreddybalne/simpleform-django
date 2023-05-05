from api.serializers.constants import Q_LONG_TEXT, Q_SHORT_TEXT
from app.models.constants import TEXT_QUESTION_TYPE_SHORT
from api.serializers.common import CommonQuestionCREATEClass
from rest_framework import serializers
from app.models import (TextQuestion, )
from .transition import TransitionDETAILSerializer
from .utils import add_all_transition

class TextQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextQuestion
        fields = '__all__'

class TextQuestionDETAILSerializer(TextQuestionSerializer):
    qtype = serializers.SerializerMethodField()
    child_transitions = TransitionDETAILSerializer(many=True)

    class Meta:
        model = TextQuestion
        fields = ('id', 'simpleform', 'qtype', 'text_type', 'title', 'sub_title', 'placeholder', 'rank', 'child_transitions', 'date_created', 'date_modified')

    def get_qtype(self, obj):
        if obj.text_type==TEXT_QUESTION_TYPE_SHORT:
            return Q_SHORT_TEXT
        return Q_LONG_TEXT 


class TextQuestionLISTSerializer(TextQuestionSerializer):
    pass

class TextQuestionCREATESerializer(TextQuestionSerializer, CommonQuestionCREATEClass):
    class Meta:
        model = TextQuestion
        fields = CommonQuestionCREATEClass.Meta.fields + ('text_type', 'placeholder', )

    def to_representation(self, instance, *args):
        return TextQuestionDETAILSerializer(instance=instance).data

    def create(self, validated_data):
        instance = super().create(validated_data)
        add_all_transition(instance.id)
        return instance

class TextQuestionUPDATESerializer(TextQuestionSerializer):
    pass
