from dependency_injector import containers, providers

from app.authentication.application.use_cases import LoginUseCase, RefreshTokenUseCase
from app.authentication.infrastructure.repository import RefreshTokenRepository
from app.authentication.infrastructure.servicies import TokenService


class AuthContainer(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()

    token_repo = providers.Factory(RefreshTokenRepository)

    token_service = providers.Factory(TokenService)

    login_use_case = providers.Factory(
        LoginUseCase,
        user_repo=core.user_repo,
        token_repo=token_repo,
        token_service=token_service,
        hash_service=core.hash_service,
    )

    refresh_token_use_case = providers.Factory(
        RefreshTokenUseCase,
        user_repo=core.user_repo,
        token_repo=token_repo,
        token_service=token_service,
    )
