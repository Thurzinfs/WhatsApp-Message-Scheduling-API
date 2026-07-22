from abc import ABC, abstractmethod


class IHashService(ABC):
    @abstractmethod
    def hash(self, value: str) -> str:
        pass

    @abstractmethod
    def verify(self, value: str, hashed_value: str) -> bool:
        pass
