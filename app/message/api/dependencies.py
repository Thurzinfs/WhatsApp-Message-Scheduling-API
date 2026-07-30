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
)
from app.message.infrastructure.repository import MessagesRepository


class MessageContainer(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()

    message_repo = providers.Factory(MessagesRepository)

    send_task_adapter = providers.Factory(TaskSendMessageAdapter)

    list_messages_schedule = providers.Factory(
        ListMessagesToSendUseCase, message_repo=message_repo
    )

    send_message_use_case = providers.Factory(
        SendMessageUseCase, message_repo=message_repo, sender=core.waha_adapter
    )

    register_message_use_case = providers.Factory(
        RegisterMessageUseCase, message_repo=message_repo, user_repo=core.user_repo
    )

    response_message_by_id = providers.Factory(
        ResponseMessageByIDUseCase, message_repo=message_repo
    )

    list_messages_by_number = providers.Factory(
        ResponseMessageByNumber, message_repo=message_repo
    )
