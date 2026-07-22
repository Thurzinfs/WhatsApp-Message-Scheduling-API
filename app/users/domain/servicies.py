from abc import ABC, abstractmethod

from app.users.domain.entities import UserEntity, RefreshTokenEntity


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


class IHashService(ABC):
    @abstractmethod
    def hash(self, raw_password: str) -> str:
        ...

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        ...
