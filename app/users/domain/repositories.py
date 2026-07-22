from abc import ABC, abstractmethod
from uuid import UUID

from app.users.domain.entities import RefreshTokenEntity, UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def save(self, entity: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> UserEntity | None:
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> UserEntity | None:
        ...

    @abstractmethod
    def verify_email_exists(self, email: str) -> bool:
        ...

    @abstractmethod
    def verify_user_exists(self, id: UUID) -> bool:
        ...


class IRefreshTokenRepository(ABC):
    @abstractmethod
    def save(self, entity: RefreshTokenEntity) -> RefreshTokenEntity:
        ...

    @abstractmethod
    def find_by_hash(self, hash: str) -> RefreshTokenEntity | None:
        ...

    @abstractmethod
    def revoke_all_by_user(self, user_id: UUID) -> None:
        ...
