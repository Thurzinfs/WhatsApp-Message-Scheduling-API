from datetime import datetime
from typing import List
from uuid import UUID

from app.message.domain.entities import MessageEntity
from app.message.domain.repositories import IMessagesRepository
from app.message.domain.role import StatusMessage
from app.message.domain.value_object import ScheduledAtTime
from app.message.infrastructure.models import Message


class MessagesRepository(IMessagesRepository):
    def save(self, message: MessageEntity) -> MessageEntity:
        Message.objects.update_or_create(
            id=message.id,
            defaults={
                'message': message.message,
                'scheduled_at': message.scheduled_at.value if message.scheduled_at else None,
                'number': message.number,
                'session': message.session,
                'status': message.status,
                'created_at': message.created_at,
            },
        )

        return message

    def find_by_id(self, id: UUID) -> MessageEntity | None:
        try:
            return self._to_model(Message.objects.get(id=id))

        except Message.DoesNotExist:
            return None

    def find_by_number(self, number: str) -> List[MessageEntity]:
        try:
            return [
                self._to_model(model)
                for model in Message.objects.filter(number=number).all()
            ]

        except Message.DoesNotExist:
            return []

    def list_messages_by_time(self, now: ScheduledAtTime) -> List[MessageEntity]:
        return [
            self._to_model(model)
            for model in Message.objects.filter(
                scheduled_at__lte=now.value, status=StatusMessage.pending
            ).all()
        ]

    def list_messages_by_number(self, number: str) -> List[MessageEntity]:
        return [
            self._to_model(model)
            for model in Message.objects.filter(number=number).all()
        ]

    def verify_exists_number(self, number: str) -> bool:
        return Message.objects.filter(number=number).exists()

    def _to_model(self, model: Message) -> MessageEntity:
        return MessageEntity(
            id=model.id,
            message=model.message,
            scheduled_at=ScheduledAtTime(value=model.scheduled_at) if model.scheduled_at else None,
            number=model.number,
            session=model.session,  # type: ignore
            status=model.status,
            created_at=model.created_at,
        )
