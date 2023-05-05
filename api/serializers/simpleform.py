from rest_framework import serializers
from app.models import (SimpleForm, TextQuestion)
from .base_question import (BaseQuestionDETAILSerializer, )

class SimpleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleForm
        fields = '__all__'

class SimpleFormDETAILSerializer(SimpleFormSerializer):
    questions = serializers.SerializerMethodField()
    workspace = serializers.SerializerMethodField()
    # questions = BaseQuestionDETAILSerializer(many=True)
    
    class Meta:
        fields = ('id', 'title', 'workspace', 'is_published', 'date_created', 'questions')
        model = SimpleForm

    def get_workspace(self, obj):
        return obj.workspace.title if obj.workspace else None

    def get_questions(self, obj):
        questions = obj.questions.all().order_by('rank')
        return BaseQuestionDETAILSerializer(questions, many=True).data

class SimpleFormLISTSerializer(SimpleFormDETAILSerializer):
    pass


class SimpleFormCREATESerializer(SimpleFormSerializer):
    
    def create(self, validated_data):
        instance = super().create(validated_data)
        TextQuestion.objects.create(simpleform=instance, rank="nnnnn")
        return instance

class SimpleFormUPDATESerializer(SimpleFormSerializer):
    
    class Meta:
        fields = ('id', 'title', 'workspace', 'is_published')
        model = SimpleForm
