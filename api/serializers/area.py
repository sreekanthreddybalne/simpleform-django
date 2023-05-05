from rest_framework import serializers
from app.models import (Area, )

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class AreaLISTSerializer(AreaSerializer):
    pass

class AreaDETAILSerializer(AreaSerializer):
    pass

class AreaCREATESerializer(AreaSerializer):
    pass

class AreaUPDATESerializer(AreaSerializer):
    pass
