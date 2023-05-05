from django.conf import settings
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import app_socket.routing
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from app.models import User, TokenBlackList
import jwt

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()
        headers = dict(scope['headers'])
        query = dict((x.split('=') for x in scope['query_string'].decode().split("&")))
        token = query['token']
        try:
            #token_name, token = headers[b'authorization'].decode().split()
            if token is None or token == "null" or token.strip() == "" or TokenBlackList.objects.filter(token=token).exists():
                raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')
            decoded = jwt.decode(token, settings.SECRET_KEY)
            username = decoded['username']
            print(username)
            user_obj=  User.objects.filter(email=username).first() or User.objects.filter(code=username).first()
            print(user_obj)
            scope['user'] = user_obj
        except:
            scope['user'] = AnonymousUser()
        if not scope["user"]: scope["user"] = AnonymousUser()
        scope["token"]=token
        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            app_socket.routing.websocket_urlpatterns
        )
    ),
})
