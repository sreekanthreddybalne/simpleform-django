from app.models.main import Briefing, SimpleForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from datetime import date, datetime, time, timedelta
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()
from api.permissions import AdminOnlyPOSTPermission

class BriefingView(APIView):
    permission_classes = (AdminOnlyPOSTPermission, )
    
    def get(self, request):
        datestr = request.query_params.get('date')
        cur_date = datetime.fromisoformat(datestr) if datestr else datetime.now()
        briefing = Briefing.objects.filter(date_created__date=cur_date.date()).first()
        if briefing:
            return Response({"description": briefing.description})
        return Response({"description": ""})

    def post(self, request):
        user = request.user
        # if not user or not user.is_authenticated:
        #     return Response(None)
        description = request.data.get("description")
        if not description:
            return Response(None)
        cur_date = datetime.now()
        briefing = Briefing.objects.filter(date_created__date=cur_date.date()).first()
        if briefing:
            briefing.description = description
        else:
            briefing = Briefing.objects.create(description=description)
        briefing.save()
        return Response({"description": description})