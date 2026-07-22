from datetime import datetime, timedelta, timezone
from uuid import uuid4

from passlib.context import CryptContext

from app.users.domain.entities import UserEntity, RefreshTokenEntity
from app.users.domain.servicies import IHashService, ITokenService

from config import settings

import jwt

from core.exceptions import BaseDomainException


class TokenService(ITokenService):
    def generate_access_token(self, user: UserEntity) -> str:
        payload = {
            'sub': str(user.id),
            'email': user.email,
            'session': user.session,
            'exp': datetime.now(timezone.utc)
            + timedelta(minutes=settings.JWT_EXP_MINUTES),
        }
        return jwt.encode(
            payload=payload,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHIM,
        )

    def generate_refresh_token(
        self, user: UserEntity
    ) -> tuple[str, RefreshTokenEntity]:
        raw_token = str(uuid4())

        hash_token = self.hash_token(raw_token)

        refresh = RefreshTokenEntity(
            token=hash_token,
            user=user.id,
            expire_at=datetime.now() + timedelta(days=settings.JWT_EXP_DAYS),
        )

        return raw_token, refresh

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHIM],
            )

        except jwt.ExpiredSignatureError:
            raise BaseDomainException('token expired')

    def hash_token(self, raw_token: str) -> str:
        import hashlib

        return hashlib.sha256(raw_token.encode()).hexdigest()


pwd_context = CryptContext(schemes=['bcrypt'])


class HashService(IHashService):
    def hash(self, raw_password: str) -> str:
        return pwd_context.hash(raw_password)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(raw_password, hashed_password)
