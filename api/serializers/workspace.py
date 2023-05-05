from rest_framework import serializers
from app.models import (Workspace, )
class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

class WorkspaceDETAILSerializer(WorkspaceSerializer):
    
    class Meta:
        fields = ('id', 'title',  'date_created')
        model = Workspace

class WorkspaceLISTSerializer(WorkspaceDETAILSerializer):
    pass


class WorkspaceCREATESerializer(WorkspaceSerializer):
    pass

class WorkspaceUPDATESerializer(WorkspaceSerializer):
    pass
