from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr

from app.users.application.dto import (
    ContactInDTO,
    ContactUpdateInDTO,
    ContactOutDTO,
    RequestCodeOutDTO,
    UserInDTO,
)


class UserInSchema(Schema):
    name: str
    email: EmailStr
    password: str
    phone: str

    def to_dto(self) -> UserInDTO:
        return UserInDTO(
            name=self.name,
            email=str(self.email),
            password=self.password,
            phone=self.phone,
        )


class UserOutSchema(Schema):
    id: UUID
    name: str
    email: str
    phone: Optional[str] = None
    connected: bool
    session: str
    session_started: bool
    access_contacts: bool
    created_at: datetime
    deleted_at: datetime | None = None

    @classmethod
    def from_domain(cls, user_dto):
        return cls(
            id=user_dto.id,
            name=user_dto.name,
            email=user_dto.email,
            phone=user_dto.phone,
            connected=user_dto.connected,
            session=user_dto.session,
            session_started=user_dto.session_started,
            access_contacts=user_dto.access_contacts,
            created_at=user_dto.created_at,
            deleted_at=user_dto.deleted_at,
        )


class ContactInSchema(Schema):
    name: str
    number: str
    user: UUID

    def to_dto(self) -> ContactInDTO:
        return ContactInDTO(
            name=self.name,
            number=self.number,
            user=self.user
        )


class ContactOutSchema(Schema):
    id: UUID
    contact_id: str
    name: str
    number: str
    user: UUID

    @staticmethod
    def from_domain(dto: ContactOutDTO):
        return ContactOutSchema(
            id=dto.id,
            contact_id=dto.contact_id,
            name=dto.name,
            number=dto.number,
            user=dto.user
        )


class ContactUpdateSchema(Schema):
    name: Optional[str] = None

    def to_dto(self) -> ContactUpdateInDTO:
        return ContactUpdateInDTO(
            name=self.name
        )


class QrCodeOutSchema(Schema):
    connected: bool
    qr_code_base64: Optional[str] = None


class RequestCodeOutSchema(Schema):
    code: str

    @staticmethod
    def from_domain(dto: RequestCodeOutDTO):
        return RequestCodeOutSchema(code=dto.code)
