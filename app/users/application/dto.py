from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserInDTO(BaseModel):
    name: str
    email: str
    password: str
    phone: str


class UserOutDTO(BaseModel):
    id: UUID
    name: str
    email: str
    phone: Optional[str] = None
    connected: bool
    session: str
    session_started: bool
    access_contacts: bool
    created_at: str
    deleted_at: str | None = None

    @classmethod
    def from_domain(cls, user_entity):
        return cls(
            id=user_entity.id,
            name=user_entity.name,
            email=user_entity.email,
            phone=user_entity.phone,
            connected=user_entity.connected,
            session=user_entity.session,
            session_started=user_entity.session_started,
            access_contacts=user_entity.access_contacts,
            created_at=user_entity.created_at.isoformat(),
            deleted_at=user_entity.deleted_at.isoformat()
            if user_entity.deleted_at
            else None,
        )


class ContactInDTO(BaseModel):
    name: str
    number: str
    user: UUID


class ContactOutDTO(BaseModel):
    id: UUID
    contact_id: str
    name: str
    number: str
    user: UUID

    @classmethod
    def from_domain(cls, contact_entity):
        return cls(
            id=contact_entity.id,
            contact_id=contact_entity.contact_id,
            name=contact_entity.name,
            number=contact_entity.number,
            user=contact_entity.user
        )


class ContactUpdateInDTO(BaseModel):
    name: Optional[str] = None


class QrCodeOutDTO(BaseModel):
    connected: bool
    qr_code_base64: Optional[str] = None


class RequestCodeOutDTO(BaseModel):
    code: str
