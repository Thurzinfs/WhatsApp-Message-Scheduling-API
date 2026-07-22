from datetime import datetime
from uuid import UUID

from app.message.application.dto import MessageInDTO, MessageOutDTO
from app.message.domain.entities import MessageEntity
from app.message.domain.exceptions import MessageNotFoundException
from app.message.domain.i_adapters import IWahaMessageAdapter
from app.message.domain.repositories import IMessagesRepository
from app.message.domain.role import StatusMessage
from app.message.domain.value_object import ScheduledAtTime

from django.utils import timezone

from app.users.domain.exceptions import UserNotFoundException
from app.users.domain.repositories import IUserRepository


class ListMessagesToSendUseCase:
    def __init__(self, message_repo: IMessagesRepository) -> None:
        self.message_repo = message_repo

    def execute(self):
        messages = self.message_repo.list_messages_by_time(
            now=ScheduledAtTime(value=timezone.localtime(timezone.now()))
        )
        if not messages:
            return []

        return messages


class SendMessageUseCase:
    def __init__(
        self,
        message_repo: IMessagesRepository,
        sender: IWahaMessageAdapter,
    ) -> None:
        self.message_repo = message_repo
        self.sender = sender

    def execute(self, id: UUID):
        message = self.message_repo.find_by_id(id)
        if not message:
            return

        self.message_repo.save(message)
        self.sender.send_message(message.number, message.message, message.session)
        
        message.change_status(StatusMessage.sent)


class RegisterMessageUseCase:
    def __init__(self, message_repo: IMessagesRepository, user_repo: IUserRepository) -> None:
        self.message_repo = message_repo
        self.user_repo = user_repo

    def execute(self, dto: MessageInDTO, user_id: UUID):
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundException('user not found')

        message = MessageEntity(
            message=dto.message,
            number=dto.number,
            session=user.session,
            status=StatusMessage.pending,
            scheduled_at=ScheduledAtTime(value=dto.scheduled_at),
        )

        self.message_repo.save(message)
        return MessageOutDTO.from_domain(message)


class ResponseMessageByNumber:
    def __init__(self, message_repo: IMessagesRepository) -> None:
        self.message_repo = message_repo

    def execute(self, number: str):
        numbers = self.message_repo.list_messages_by_number(number)
        if not numbers:
            return []

        return [MessageOutDTO.from_domain(message) for message in numbers]


class ResponseMessageByIDUseCase:
    def __init__(self, message_repo: IMessagesRepository) -> None:
        self.message_repo = message_repo

    def execute(self, id: UUID):
        message = self.message_repo.find_by_id(id)
        if not message:
            raise MessageNotFoundException('message not found')

        return MessageOutDTO.from_domain(message)
