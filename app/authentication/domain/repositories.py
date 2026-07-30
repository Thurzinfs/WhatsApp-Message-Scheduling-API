from abc import ABC, abstractmethod
from uuid import UUID

from app.authentication.domain.entities import RefreshTokenEntity


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
