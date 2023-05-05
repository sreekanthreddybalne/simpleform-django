from api.serializers.constants import Q_PHONE_NUMBER
from api.serializers.common import CommonQuestionCREATEClass
from rest_framework import serializers
from app.models import (PhoneQuestion, )

class PhoneQuestionSerializer(serializers.ModelSerializer):
    qtype = serializers.ReadOnlyField(default=Q_PHONE_NUMBER)

    class Meta:
        model = PhoneQuestion
        fields = ('id', 'simpleform', 'qtype', 'title', 'sub_title', 'rank', 'date_created', 'date_modified')

class PhoneQuestionLISTSerializer(PhoneQuestionSerializer):
    pass

class PhoneQuestionDETAILSerializer(PhoneQuestionSerializer):
    pass

class PhoneQuestionCREATESerializer(PhoneQuestionSerializer, CommonQuestionCREATEClass):

    class Meta(CommonQuestionCREATEClass.Meta):
        model = PhoneQuestion
        
    def to_representation(self, instance, *args):
        return PhoneQuestionDETAILSerializer(instance=instance).data

class PhoneQuestionUPDATESerializer(PhoneQuestionSerializer):
    pass
