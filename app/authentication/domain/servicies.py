from abc import ABC, abstractmethod

from app.authentication.domain.entities import RefreshTokenEntity
from app.users.domain.entities import UserEntity


class ITokenService(ABC):
    @abstractmethod
    def generate_access_token(self, user: UserEntity) -> str:
        ...

    @abstractmethod
    def generate_refresh_token(
        self, user: UserEntity
    ) -> tuple[str, RefreshTokenEntity]:
        ...

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        ...

    @abstractmethod
    def hash_token(self, raw_token: str) -> str:
        ...
