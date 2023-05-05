from rest_framework import serializers
from app.models import (User, )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserDETAILSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)

class UserLISTSerializer(UserDETAILSerializer):
    pass

class UserCREATESerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)

    def to_representation(self, instance, *args):
        return UserDETAILSerializer(instance=instance).data

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

class UserUPDATESerializer(UserSerializer):
    
    def to_representation(self, instance, *args):
        return UserDETAILSerializer(instance=instance).data

