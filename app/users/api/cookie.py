from typing import Any

from django.http import HttpRequest
import jwt
from ninja.security import APIKeyCookie

from app.users.infrastructure.models import User
from config import settings
from core.exceptions import BaseDomainException

class AuthCookie(APIKeyCookie):
    param_name = 'auth_token'

    def authenticate(self, request: HttpRequest, key: str) -> Any | None:
        try:
            payload = jwt.decode(
                key, 
                settings.JWT_SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHIM]
            )

            user = User.objects.get(id=payload['sub'])
            if not user:
                raise BaseDomainException('user not found')
            
            return user

        except (jwt.PyJWTError, User.DoesNotExist):
            return None
