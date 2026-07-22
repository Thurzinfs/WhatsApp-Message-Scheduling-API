from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.message.domain.role import StatusMessage
from app.message.domain.value_object import ScheduledAtTime
from core.exceptions import FieldRequiredException


@dataclass
class MessageEntity:
    id: UUID = field(default_factory=uuid4)
    message: str = field(default='')
    scheduled_at: ScheduledAtTime | None = field(default=None)
    number: str = field(default='')
    session: str = field(default='')
    status: StatusMessage | str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)

    def change_number(self, number: str):
        if not number:
            raise FieldRequiredException('field number is required')

        self.number = number

    def change_message(self, message: str):
        if not message:
            raise FieldRequiredException('field message is required')

        self.message = message

    def change_status(self, status: str):
        if not status:
            raise FieldRequiredException('field status is required')

        self.status = status
