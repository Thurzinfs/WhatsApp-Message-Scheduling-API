from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.message.domain.entities import MessageEntity
from app.message.domain.value_object import ScheduledAtTime


class IMessagesRepository(ABC):
    @abstractmethod
    def save(self, message: MessageEntity) -> MessageEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> MessageEntity | None:
        ...

    @abstractmethod
    def find_by_number(self, number: str) -> List[MessageEntity]:
        ...

    @abstractmethod
    def list_messages_by_time(self, now: ScheduledAtTime) -> List[MessageEntity]:
        ...

    @abstractmethod
    def list_messages_by_number(self, number: str) -> List[MessageEntity]:
        ...

    @abstractmethod
    def verify_exists_number(self, number: str) -> bool:
        ...
