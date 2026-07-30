from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.users.domain.entities import ContactEntity


class IHashService(ABC):
    @abstractmethod
    def hash(self, raw_password: str) -> str:
        ...

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        ...


class IFilterContactsService(ABC):
    @abstractmethod
    def list_contacts(self, contacts_list: List, id: UUID) -> List[ContactEntity]:
        ...
