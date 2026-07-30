from pydantic import BaseModel


class LoginInDTO(BaseModel):
    email: str
    password: str


class LoginOutDTO(BaseModel):
    access_token: str
    refresh_token: str
