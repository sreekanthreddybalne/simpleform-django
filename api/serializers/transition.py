from rest_framework import serializers
from app.models import (Transition, PhoneQuestion)

class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = '__all__'

class TransitionLISTSerializer(TransitionSerializer):
    pass

class TransitionDETAILSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "to_question", "to_question", "on_value", "is_end")
        model = Transition


class TransitionCREATESerializer(TransitionSerializer):

    def validate(self, attrs):
        from_question = attrs["from_question"]
        to_question = attrs.get("to_question")
        if from_question == to_question:
            raise serializers.ValidationError("Both questions in a transition cannot be same.")
        if to_question and (from_question.simpleform != to_question.simpleform):
            raise serializers.ValidationError("Both questions should belong to a single form.")
        if from_question.child_transitions.filter(on_value=attrs["on_value"]).exists():
            raise serializers.ValidationError("A transition already exists for the question and value.")
        return attrs

class TransitionUPDATESerializer(TransitionCREATESerializer):
    
    def validate(self, attrs):
        instance = self.instance
        from_question = attrs["from_question"]
        to_question = attrs.get("to_question")
        if from_question == to_question:
            raise serializers.ValidationError("Both questions in a transition cannot be same.")
        if to_question and (from_question.simpleform != to_question.simpleform):
            raise serializers.ValidationError("Both questions should belong to a single form.")
        if from_question.child_transitions.filter(on_value=attrs["on_value"]).exclude(id=instance.id).exists():
            raise serializers.ValidationError("A transition already exists for the question and value.")
        return attrs
