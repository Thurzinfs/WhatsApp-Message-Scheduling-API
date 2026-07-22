from app.message.domain.servicies import IHashService

from passlib.context import CryptContext


class HashService(IHashService):
    def __init__(self):
        self._context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def hash(self, value: str) -> str:
        return self._context.hash(value)

    def verify(self, value: str, hashed_value: str) -> bool:
        return self._context.verify(value, hashed_value)
