from app.models.main import SimpleForm
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import (UserDETAILSerializer,)
from rest_framework import permissions
class AuthenticatedUserView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            return Response(None)
        print(UserDETAILSerializer(instance=user).data)
        return Response(UserDETAILSerializer(instance=user).data)

class DuplicateSimpleformView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        user = request.user
        # if not user or not user.is_authenticated:
        #     return Response(None)
        simpleform_id = request.data.get("id", None)
        if not simpleform_id:
            return Response(None)
        simpleform = SimpleForm.objects.get(pk=simpleform_id)
        simpleform.pk = None
        simpleform = simpleform.save()
        
        print(UserDETAILSerializer(instance=user).data)
        return Response(UserDETAILSerializer(instance=user).data)