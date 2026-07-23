from abc import ABC, abstractmethod
from uuid import UUID


class IContactsSyncTaskAdapter(ABC):
    @abstractmethod
    def sync(self, id: UUID):
        ...
