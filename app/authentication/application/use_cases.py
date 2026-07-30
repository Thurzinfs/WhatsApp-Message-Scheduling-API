from app.authentication.application.dto import LoginInDTO, LoginOutDTO
from app.authentication.domain.repositories import IRefreshTokenRepository
from app.authentication.domain.servicies import ITokenService
from app.message.domain.servicies import IHashService
from app.users.domain.exceptions import UserNotFoundException
from app.users.domain.repositories import IUserRepository
from core.exceptions import BaseDomainException


class LoginUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        token_repo: IRefreshTokenRepository,
        token_service: ITokenService,
        hash_service: IHashService,
    ) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.token_service = token_service
        self.hash_service = hash_service

    def execute(self, dto: LoginInDTO):
        user = self.user_repo.find_by_email(dto.email)
        if not user:
            raise UserNotFoundException('user not found')

        if not self.hash_service.verify(dto.password, user.password):
            raise BaseDomainException('invalid credentials')

        access_token = self.token_service.generate_access_token(user)
        (raw_refresh, entity) = self.token_service.generate_refresh_token(user)
        self.token_repo.save(entity)

        return LoginOutDTO(
            access_token=access_token, refresh_token=raw_refresh
        )


class RefreshTokenUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        token_repo: IRefreshTokenRepository,
        token_service: ITokenService,
    ) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.token_service = token_service

    def execute(self, token: str | None):
        if not token:
            raise BaseDomainException('token not found')
        
        refresh = self.token_repo.find_by_hash(token)
        if not refresh:
            raise BaseDomainException('invalid refresh token')

        if refresh.is_valid():
            raise BaseDomainException('refresh token expired')

        if not refresh.user:
            raise BaseDomainException('refresh token has no user')

        user = self.user_repo.find_by_id(refresh.user)
        if not user:
            raise UserNotFoundException('user not found')
        
        new_access_token = self.token_service.generate_access_token(user)
        return new_access_token
