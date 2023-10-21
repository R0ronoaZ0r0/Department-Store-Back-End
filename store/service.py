from datetime import datetime
import jwt
from sequences import get_next_value

from store.serializers import UserLoginSerializer
from dept_store import settings


class AuthenticationUtils:

    @classmethod
    def get_user_claims(cls, authenticated_user):
        return {
            'claims': UserLoginSerializer(authenticated_user).data
        }

    @classmethod
    def get_user_access_token(cls, user_claims):
        claims_obj = {
            **user_claims,
            'type': 'access',
            'exp': datetime.utcnow() + settings.JWTConfig['ACCESS_TOKEN_LIFETIME']
        }

        return jwt.encode(claims_obj, settings.JWTConfig['SIGNING_KEY'], settings.JWTConfig['ALGORITHM'])

    @classmethod
    def get_user_refresh_token(cls, user_claims):
        claims_obj = {
            **user_claims,
            'type': 'refresh',
            'exp': datetime.utcnow() + settings.JWTConfig['REFRESH_TOKEN_LIFETIME']
        }

        return jwt.encode(claims_obj, settings.JWTConfig['SIGNING_KEY'], settings.JWTConfig['ALGORITHM'])


class OrderUtils:

    @classmethod
    def get_next_order_id(cls):
        return get_next_value('order_number', 20000)
