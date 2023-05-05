from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework import authentication, exceptions, serializers
from django.contrib.auth.models import AnonymousUser
import json
import urllib # Python URL functions
import urllib.request, urllib.error, urllib.parse
User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
# from .serializers import AuthUserSerializer
from app.tasks import task_send_activation_mail, task_send_welcome_mail
from api.utils import generate_random_string

def jwt_response_payload_handler(token, user=AnonymousUser(), request=None):
    return {
        'token': token,
        # **AuthUserSerializer(user, context={'request': request}).data
    }


class CustomJWTSerializer(JSONWebTokenSerializer):
    username_field = 'username'

    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(username=attrs.get("username")).first()
        if user_obj is not None:
            credentials = {
                'username':user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                print(type(user))
                if user:
                    if not user.is_active:
                        msg = _('Account is disabled')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = _('Invalid Credentials')
                    raise serializers.ValidationError(msg)

            else:
                msg = _('Must include "{username_field}" and "password"')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)

        else:
            msg = _('Account does not exist')
            raise serializers.ValidationError(msg)

from rest_framework.authentication import get_authorization_header

import jwt

class JWTAuthentication(authentication.TokenAuthentication):
    USERNAME_FIELDS = ["username"]

    def get_token_from_auth_header(self, auth):
        auth = auth.split()
        if not auth or auth[0].lower() != b'bearer':
            return None
        try:
            return auth[1].decode()
        except:
            return None

    def authenticate(self, request): # it will return user object
        auth = get_authorization_header(request)
        token = self.get_token_from_auth_header(auth)
        try:
            if token is None or token == "null" or token.strip() == "":
                raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')
            decoded = jwt.decode(token, settings.SECRET_KEY)
            username = decoded['username']
            user_obj = User.objects.filter(username=username).first()
        except:
            user_obj = AnonymousUser()
        print(user_obj)
        return (user_obj, AnonymousUser())
        """except jwt.ExpiredSignature :
            raise exceptions.AuthenticationFailed('Token Expired, Please Login')
        except jwt.DecodeError :
            raise exceptions.AuthenticationFailed('Token Modified by thirdparty')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid Token')
        except Exception as e:
            raise exceptions.AuthenticationFailed(e)
        return (user_obj, None)"""

    def get_user(self, userid):
        try:
            return User.objects.get(pk=userid)
        except Exception as e:
            return AnonymousUser()
