from typing import Optional
from uuid import UUID

from ninja import Schema

from datetime import datetime

from app.message.application.dto import MessageInDTO, MessageOutDTO
from app.message.domain.role import StatusMessage
from app.message.domain.value_object import ScheduledAtTime


class MessageInSchema(Schema):
    message: str
    scheduled_at: datetime
    number: str

    def to_dto(self) -> MessageInDTO:
        return MessageInDTO(
            message=self.message, scheduled_at=self.scheduled_at, number=self.number
        )


class MessageOutSchema(Schema):
    id: UUID
    message: str
    scheduled_at: datetime
    number: str
    session: str
    status: StatusMessage
    created_at: datetime

    @staticmethod
    def from_domain(dto: MessageOutDTO):
        return MessageOutSchema(
            id=dto.id,
            message=dto.message,
            scheduled_at=dto.scheduled_at,
            number=dto.number,
            session=dto.session,
            status=dto.status,
            created_at=dto.created_at,
        )


class UpdateInSchema(Schema):
    number: Optional[str] = None
    message: Optional[str] = None
