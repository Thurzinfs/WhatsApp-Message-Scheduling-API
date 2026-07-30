from typing import List
from uuid import UUID
from passlib.context import CryptContext

from app.users.domain.entities import ContactEntity
from app.users.domain.servicies import IFilterContactsService, IHashService


pwd_context = CryptContext(schemes=['bcrypt'])


class HashService(IHashService):
    def hash(self, raw_password: str) -> str:
        return pwd_context.hash(raw_password)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(raw_password, hashed_password)


class FilterContactsService(IFilterContactsService):
    def list_contacts(self, contacts_list: List, id: UUID) -> List[ContactEntity]:
        filters = []

        for contact in contacts_list:
            name = contact.get('name') or contact.get('pushname')
            contact_id = contact.get('id')
            number = contact.get('number')

            if not all([name, contact_id, number]):
                continue

            filters.append(ContactEntity(
                contact_id=contact_id,
                name=name,
                number=number,
                user=id
            ))

        print(f"[DEBUG] use case filter list: {filters}")

        return filters
