from ninja import Schema
from pydantic import EmailStr

from app.authentication.application.dto import LoginInDTO, LoginOutDTO


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
