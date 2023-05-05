
from rest_framework import serializers
from app.models.main import BaseQuestion, SimpleForm
import pyranker

class CommonQuestionCREATEClass(serializers.ModelSerializer):
    previous_question = serializers.PrimaryKeyRelatedField(queryset=BaseQuestion.objects.all(), allow_null=True)

    class Meta:
        model = BaseQuestion
        fields = ('simpleform', 'previous_question', 'title', 'sub_title')

    def validate(self, attrs):
        simpleform: SimpleForm = attrs["simpleform"]
        previous_question: BaseQuestion = attrs.pop("previous_question", None)
        next_question_fq = None
        next_question: BaseQuestion = None
        if previous_question:
            if previous_question.simpleform!=simpleform:
                raise serializers.ValidationError({'previous_question': "Invalid previous question"})
            next_question_fq = BaseQuestion.objects.filter(simpleform=simpleform, rank__gt=previous_question.rank).order_by('rank')
        else:
            next_question_fq = BaseQuestion.objects.filter(simpleform=simpleform).order_by('rank')
        if hasattr(self, "instance") and self.instance:
            next_question = next_question_fq.exclude(pk=self.instance.id).first()
        else:
            next_question = next_question_fq.first()
        previous_question_rank = previous_question.rank if previous_question else None
        next_question_rank = next_question.rank if next_question else None
        attrs["rank"] = pyranker.get_rank(previous_question_rank, next_question_rank, start_length=10)
        return attrs