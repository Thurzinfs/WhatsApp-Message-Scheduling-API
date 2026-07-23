from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.users.domain.entities import ContactEntity, RefreshTokenEntity, UserEntity
from app.users.domain.value_objects import PhoneNumberVO


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


class IContactsRepository(ABC):
    @abstractmethod
    def save(self, entity: ContactEntity) -> ContactEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> ContactEntity | None:
        ...

    @abstractmethod
    def verify_by_id_waha(self, id_waha: str) -> ContactEntity | None:
        ...

    @abstractmethod
    def find_by_number(self, number: PhoneNumberVO) -> ContactEntity | None:
        ...

    @abstractmethod
    def list_by_user(self, id: UUID) -> List[ContactEntity]:
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
