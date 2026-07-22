from dependency_injector import containers, providers

from app.users.application.use_cases import (
    DeactiveUserUseCase,
    LoginUseCase,
    LoginWahaForWhatsAppQrCodeUseCase,
    RegisterUserUseCase,
    RequestCodeLoginWhatsAppUseCase,
    ResponseUserByEmailUseCase,
    ResponseUserByIDUseCase,
)
from app.users.infrastructure.repository import (
    RefreshTokenRepository,
    UserRepository,
)
from app.users.infrastructure.services import HashService, TokenService


class UserContainer(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()

    user_repo = providers.Factory(UserRepository)

    token_repo = providers.Factory(RefreshTokenRepository)

    token_service = providers.Factory(TokenService)

    hash_service = providers.Factory(HashService)

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
        DeactiveUserUseCase, user_repo=user_repo, waha_adapter=core.waha_adapter
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
