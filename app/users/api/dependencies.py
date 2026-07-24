from dependency_injector import containers, providers

from app.users.application.use_cases import (
    DeactiveUserUseCase,
    EnableSyncContactsUseCase,
    ListContactsByUserUseCase,
    LoginUseCase,
    LoginWahaForWhatsAppQrCodeUseCase,
    RegisterUserUseCase,
    RequestCodeLoginWhatsAppUseCase,
    ResponseContactByIDUseCase,
    ResponseUserByEmailUseCase,
    ResponseUserByIDUseCase,
    ResponsenContactByNumberUseCase,
    SyncContactsUserUseCase,
)
from app.users.infrastructure.adapters import ContactsSyncTaskAdapter
from app.users.infrastructure.repository import (
    ContactRepository,
    RefreshTokenRepository,
    UserRepository,
)
from app.users.infrastructure.services import FilterContactsService, HashService, TokenService


class UserContainer(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()

    user_repo = providers.Factory(UserRepository)

    token_repo = providers.Factory(RefreshTokenRepository)

    contact_repo = providers.Factory(ContactRepository)

    token_service = providers.Factory(TokenService)

    hash_service = providers.Factory(HashService)

    filter_service = providers.Factory(FilterContactsService)

    task_sync_adapter = providers.Factory(ContactsSyncTaskAdapter)

    register_user_use_case = providers.Factory(
        RegisterUserUseCase,
        user_repo=user_repo,
        waha_adapter=core.waha_adapter,
        hash_service=core.hash_service,
    )

    response_user_use_case = providers.Factory(
        ResponseUserByIDUseCase, user_repo=user_repo
    )

    response_user_by_email_use_case = providers.Factory(
        ResponseUserByEmailUseCase, user_repo=user_repo
    )

    deactive_user_use_case = providers.Factory(
        DeactiveUserUseCase,
        user_repo=user_repo,
        waha_adapter=core.waha_adapter,
    )

    enable_sync_contacts_use_case = providers.Factory(
        EnableSyncContactsUseCase,
        user_repo=user_repo,
        task_sync_adapter=task_sync_adapter
    )

    sync_contacts_user_use_case = providers.Factory(
        SyncContactsUserUseCase,
        user_repo=user_repo,
        waha_adapter=core.waha_adapter,
        filter_service=filter_service,
        contact_repo=contact_repo
    )

    login_use_case = providers.Factory(
        LoginUseCase,
        user_repo=user_repo,
        token_repo=token_repo,
        token_service=token_service,
        hash_service=hash_service,
    )

    login_qrcode_waha_use_case = providers.Factory(
        LoginWahaForWhatsAppQrCodeUseCase,
        user_repo=user_repo,
        waha_adapter=core.waha_adapter,
    )

    login_code_waha_use_case = providers.Factory(
        RequestCodeLoginWhatsAppUseCase,
        user_repo=user_repo,
        waha_adapter=core.waha_adapter,
    )

    list_contacts_by_user_use_case = providers.Factory(
        ListContactsByUserUseCase,
        contact_repo=contact_repo
    )

    response_contact_by_id = providers.Factory(
        ResponseContactByIDUseCase,
        contact_repo=contact_repo
    )

    response_contact_by_number = providers.Factory(
        ResponsenContactByNumberUseCase,
        contact_repo=contact_repo
    )
