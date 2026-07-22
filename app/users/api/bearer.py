from typing import Any

from django.http import HttpRequest
import jwt
from ninja.security import HttpBearer

from app.users.infrastructure.models import User
from config import settings
from core.exceptions import BaseDomainException


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Any | None:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHIM],
            )
            user = User.objects.get(id=payload['sub'])
            if not user:
                raise BaseDomainException('user not found')

            return user

        except jwt.PyJWTError:
            return None
