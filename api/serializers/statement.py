from api.serializers.common import CommonQuestionCREATEClass
from api.serializers.constants import Q_STATEMENT
from rest_framework import serializers
from app.models import (Statement, )

class StatementSerializer(serializers.ModelSerializer):
    qtype = serializers.ReadOnlyField(default=Q_STATEMENT)

    class Meta:
        model = Statement
        fields = ('id', 'simpleform', 'qtype', 'title', 'sub_title', 'rank', 'date_created', 'date_modified')

class StatementLISTSerializer(StatementSerializer):
    pass

class StatementDETAILSerializer(StatementSerializer):
    pass

class StatementCREATESerializer(StatementSerializer, CommonQuestionCREATEClass):
    class Meta(CommonQuestionCREATEClass.Meta):
        model = Statement

    def to_representation(self, instance, *args):
        return StatementDETAILSerializer(instance=instance).data

class StatementUPDATESerializer(StatementSerializer):
    pass
