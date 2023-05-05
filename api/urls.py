from api.views.workspace import WorkspaceViewSet
from api.views.briefing import BriefingView
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, ObtainJSONWebToken
from api.views import (
    UserViewSet, AuthenticatedUserView, BaseQuestionViewSet, EmailQuestionViewSet, 
    StatementViewSet, ChoiceQuestionViewSet, TextQuestionViewSet, PhoneQuestionViewSet, SimpleFormViewSet, TransitionViewSet)
# from .jwt_utils import CustomJWTSerializer

class CustomDefaultRouter(DefaultRouter):

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

router = CustomDefaultRouter()
router.register('user', UserViewSet, basename='users')
router.register('workspace', WorkspaceViewSet, basename='workspaces')
router.register('simpleform', SimpleFormViewSet, basename='simpleforms')
router.register('baseQuestion', BaseQuestionViewSet, basename='baseQuestions')
router.register('textQuestion', TextQuestionViewSet, basename='textQuestions')
router.register('phoneQuestion', PhoneQuestionViewSet, basename='phoneQuestions')
router.register('emailQuestion', EmailQuestionViewSet, basename='emailQuestions')
router.register('statement', StatementViewSet, basename='statements')
router.register('choiceQuestion', ChoiceQuestionViewSet, basename='choiceQuestions')
router.register('transition', TransitionViewSet, basename='transitions')


urlpatterns = router.urls

from .jwt_utils import CustomJWTSerializer
urlpatterns+=[
    path(r'authenticatedUser/', AuthenticatedUserView.as_view()),
    path(r'briefing', BriefingView.as_view()),

    path(r'auth/token/', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),

]
