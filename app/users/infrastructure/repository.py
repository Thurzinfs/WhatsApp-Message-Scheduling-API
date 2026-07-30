from typing import List
from uuid import UUID

from app.users.domain.entities import ContactEntity, UserEntity
from app.users.domain.repositories import (
    IContactsRepository,
    IUserRepository,
)
from app.users.domain.value_objects import PhoneNumberVO
from app.users.infrastructure.models import Contact, User


class UserRepository(IUserRepository):
    def save(self, entity: UserEntity) -> UserEntity:
        User.objects.update_or_create(
            id=entity.id,
            defaults={
                'name': entity.name,
                'email': entity.email,
                'password': entity.password,
                'phone': entity.phone,
                'connected': entity.connected,
                'session': entity.session,
                'session_started': entity.session_started,
                'access_contacts': entity.access_contacts,
                'created_at': entity.created_at,
                'deleted_at': entity.deleted_at,
            },
        )
        return entity

    def find_by_id(self, id: UUID) -> UserEntity | None:
        try:
            return self._to_entity(User.objects.get(id=id))

        except User.DoesNotExist:
            return None

    def find_by_email(self, email: str) -> UserEntity | None:
        try:
            return self._to_entity(User.objects.get(email=email))

        except User.DoesNotExist:
            return None

    def verify_email_exists(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    def verify_user_exists(self, id: UUID) -> bool:
        return User.objects.filter(id=id).exists()

    def _to_entity(self, model: User) -> UserEntity:
        return UserEntity(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            phone=model.phone if model.phone else None,
            connected=model.connected,
            session=model.session,
            session_started=model.session_started,
            access_contacts=model.access_contacts,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
        )


class ContactRepository(IContactsRepository):
    def save(self, entity: ContactEntity) -> ContactEntity:
        Contact.objects.update_or_create(
            id=entity.id,
            defaults={
                'contact_id': entity.contact_id,
                'name': entity.name,
                'number': entity.number,
                'user_id': entity.user,
                'created_at': entity.created_at                
            }
        )

        return entity

    def find_by_id(self, id: UUID) -> ContactEntity | None:
        try:
            return self._to_entity(Contact.objects.get(id=id))

        except Contact.DoesNotExist:
            return None

    def verify_by_id_waha(self, id_waha: str) -> ContactEntity | None:
        try:
            return self._to_entity(Contact.objects.get(contact_id=id_waha))

        except Contact.DoesNotExist:
            return None
            

    def find_by_number(self, number: PhoneNumberVO) -> ContactEntity | None:
        try:
            return self._to_entity(Contact.objects.get(number=number.value))

        except Contact.DoesNotExist:
            return None

    def list_by_user(self, id: UUID) -> List[ContactEntity]:
        try:
            return [
                self._to_entity(model)
                for model in Contact.objects.filter(user=id).all()
            ]

        except Contact.DoesNotExist:
            return []

    def _to_entity(self, model: Contact) -> ContactEntity:
        return ContactEntity(
            id=model.id,
            contact_id=model.contact_id,  # type: ignore
            name=model.name,
            number=model.number,
            user=model.user.id,
            created_at=model.created_at
        )
