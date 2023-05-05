from rest_framework import serializers
from app.models import (EmailQuestion, )

class EmailQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailQuestion
        fields = '__all__'

class EmailQuestionLISTSerializer(EmailQuestionSerializer):
    pass

class EmailQuestionDETAILSerializer(EmailQuestionSerializer):
    pass

class EmailQuestionCREATESerializer(EmailQuestionSerializer):
    pass

class EmailQuestionUPDATESerializer(EmailQuestionSerializer):
    pass
