from dependency_injector import containers, providers

from app.message.application.use_cases import (
    ListMessagesToSendUseCase,
    RegisterMessageUseCase,
    ResponseMessageByIDUseCase,
    ResponseMessageByNumber,
    SendMessageUseCase,
)
from app.message.infrastructure.adapters import (
    TaskSendMessageAdapter,
    WahaMessageAdapter,
)
from app.message.infrastructure.repository import MessagesRepository
from app.users.infrastructure.repository import UserRepository


class MessageContainer(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()

    user_repo = providers.Factory(UserRepository)

    message_repo = providers.Factory(MessagesRepository)

    send_task_adapter = providers.Factory(TaskSendMessageAdapter)

    list_messages_schedule = providers.Factory(
        ListMessagesToSendUseCase, message_repo=message_repo
    )

    send_message_use_case = providers.Factory(
        SendMessageUseCase, message_repo=message_repo, sender=core.waha_adapter
    )

    register_message_use_case = providers.Factory(
        RegisterMessageUseCase, message_repo=message_repo, user_repo=user_repo
    )

    response_message_by_id = providers.Factory(
        ResponseMessageByIDUseCase, message_repo=message_repo
    )

    list_messages_by_number = providers.Factory(
        ResponseMessageByNumber, message_repo=message_repo
    )
