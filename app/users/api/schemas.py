from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr

from app.users.application.dto import (
    ContactInDTO,
    ContactUpdateInDTO,
    CotnactOutDTO,
    LoginInDTO,
    LoginOutDTO,
    QrCodeOutDTO,
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
            created_at=user_dto.created_at,
            deleted_at=user_dto.deleted_at,
        )


class ContactInSchema(Schema):
    name: str
    number: str
    lid: str
    user: UUID

    def to_dto(self) -> ContactInDTO:
        return ContactInDTO(
            name=self.name,
            number=self.number,
            lid=self.lid,
            user=self.user
        )


class ContactOutSchema(Schema):
    id: UUID
    name: str
    number: str
    lid: str
    user: UUID

    @staticmethod
    def from_domain(dto: CotnactOutDTO):
        return ContactOutSchema(
            id=dto.id,
            name=dto.name,
            number=dto.number,
            lid=dto.lid,
            user=dto.user
        )


class ContactUpdateSchema(Schema):
    name: Optional[str] = None

    def to_dto(self) -> ContactUpdateInDTO:
        return ContactUpdateInDTO(
            name=self.name
        )


class LoginInSchema(Schema):
    email: EmailStr
    password: str

    def to_dto(self) -> LoginInDTO:
        return LoginInDTO(email=str(self.email), password=self.password)


class LoginOutSchema(Schema):
    access_token: str
    refresh_token: str

    @staticmethod
    def from_domain(dto: LoginOutDTO):
        return LoginOutSchema(
            access_token=dto.access_token, refresh_token=dto.refresh_token
        )


class QrCodeOutSchema(Schema):
    connected: bool
    qr_code_base64: Optional[str] = None


class RequestCodeOutSchema(Schema):
    code: str

    @staticmethod
    def from_domain(dto: RequestCodeOutDTO):
        return RequestCodeOutSchema(code=dto.code)
