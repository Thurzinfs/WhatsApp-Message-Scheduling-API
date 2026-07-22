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
            created_at=user_entity.created_at.isoformat(),
            deleted_at=user_entity.deleted_at.isoformat()
            if user_entity.deleted_at
            else None,
        )


class ContactInDTO(BaseModel):
    name: str
    number: str
    lid: str
    user: UUID


class CotnactOutDTO(BaseModel):
    id: UUID
    name: str
    number: str
    lid: str
    user: UUID

    @classmethod
    def from_domain(cls, contact_entity):
        return cls(
            id=contact_entity.id,
            name=contact_entity.name,
            number=contact_entity.number,
            lid=contact_entity.lid,
            user=contact_entity.user
        )


class ContactUpdateInDTO(BaseModel):
    name: Optional[str] = None


class LoginInDTO(BaseModel):
    email: str
    password: str


class LoginOutDTO(BaseModel):
    access_token: str
    refresh_token: str


class QrCodeOutDTO(BaseModel):
    connected: bool
    qr_code_base64: Optional[str] = None


class RequestCodeOutDTO(BaseModel):
    code: str
