from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from datetime import datetime

from app.message.domain.role import StatusMessage
from app.message.domain.value_object import ScheduledAtTime


class MessageInDTO(BaseModel):
    message: str
    scheduled_at: datetime
    number: str


class MessageOutDTO(BaseModel):
    id: UUID
    message: str
    scheduled_at: datetime
    number: str
    session: str
    status: StatusMessage
    created_at: datetime

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            message=model.message,
            scheduled_at=model.scheduled_at.value,
            number=model.number,
            session=model.session,
            status=model.status,
            created_at=model.created_at,
        )


class UpdateMessageDTO(BaseModel):
    number: Optional[str] = None
    message: Optional[str] = None
