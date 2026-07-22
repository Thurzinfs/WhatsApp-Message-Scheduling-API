from uuid import UUID

from app.message.domain.i_adapters import IWahaMessageAdapter
from app.message.domain.servicies import IHashService
from app.users.application.dto import (
    LoginInDTO,
    LoginOutDTO,
    QrCodeOutDTO,
    RequestCodeOutDTO,
    UserInDTO,
    UserOutDTO,
)
from app.users.domain.entities import UserEntity
from app.users.domain.exceptions import UserNotFoundException
from app.users.domain.repositories import (
    IRefreshTokenRepository,
    IUserRepository,
)
from app.users.domain.servicies import ITokenService
from core.exceptions import BaseDomainException


class RegisterUserUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        waha_adapter: IWahaMessageAdapter,
        hash_service: IHashService,
    ):
        self.user_repo = user_repo
        self.waha_adapter = waha_adapter
        self.hash_service = hash_service

    def execute(self, dto: UserInDTO) -> UserOutDTO:
        if self.user_repo.verify_email_exists(dto.email):
            raise ValueError('Email already exists')

        password_hash = self.hash_service.hash(dto.password)

        user = UserEntity(
            name=dto.name,
            email=dto.email,
            password=password_hash,
            phone=dto.phone,
        )

        status = self.waha_adapter.get_session_status(user.session)

        if status is None:
            self.waha_adapter.create_session(user.session)
            self.waha_adapter.start_session(user.session)

            user.change_connection_status(True)

        elif status != 'WORKING':
            self.waha_adapter.start_session(user.session)

            user.change_connection_status(True)

        self.user_repo.save(user)

        return UserOutDTO.from_domain(user)


class ResponseUserByIDUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def execute(self, id: UUID) -> UserOutDTO:
        user = self.user_repo.find_by_id(id)
        if not user:
            raise UserNotFoundException('user not found')

        if user.deleted_at is not None:
            raise BaseDomainException('user deleted')

        return UserOutDTO.from_domain(user)


class ResponseUserByEmailUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def execute(self, email: str) -> UserOutDTO:
        user = self.user_repo.find_by_email(email)
        if not user:
            raise UserNotFoundException('user not found')

        return UserOutDTO.from_domain(user)


class DeactiveUserUseCase:
    def __init__(
        self, user_repo: IUserRepository, waha_adapter: IWahaMessageAdapter
    ) -> None:
        self.user_repo = user_repo
        self.waha_adapter = waha_adapter

    def execute(self, id: UUID):
        user = self.user_repo.find_by_id(id)
        if not user:
            raise UserNotFoundException('user not found')

        self.waha_adapter.delete_session(user.session)

        user.delete()
        self.user_repo.save(user)

        return UserOutDTO.from_domain(user)


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


class LoginWahaForWhatsAppQrCodeUseCase:
    def __init__(
        self, user_repo: IUserRepository, waha_adapter: IWahaMessageAdapter
    ) -> None:
        self.user_repo = user_repo
        self.waha_adapter = waha_adapter

    def execute(self, id: UUID):
        user = self.user_repo.find_by_id(id)
        if not user:
            raise UserNotFoundException('user not found')

        status = self.waha_adapter.get_session_status(user.session)

        if status == 'WORKING':
            return None

        if status is None:
            self.waha_adapter.create_session(user.session)
            self.waha_adapter.start_session(user.session)

        if status == 'SCAN_QR_CODE':
            self.waha_adapter.start_session(user.session)

        return self.waha_adapter.get_login_qrcode(user.session)


class RequestCodeLoginWhatsAppUseCase:
    def __init__(
        self, user_repo: IUserRepository, waha_adapter: IWahaMessageAdapter
    ) -> None:
        self.user_repo = user_repo
        self.waha_adapter = waha_adapter

    def execute(self, id: UUID):
        user = self.user_repo.find_by_id(id)
        if not user:
            raise UserNotFoundException('user not found')

        status = self.waha_adapter.get_session_status(user.session)

        if status is None:
            self.waha_adapter.create_session(user.session)
            self.waha_adapter.start_session(user.session)

        elif status == 'SCAN_QR_CODE':
            self.waha_adapter.start_session(user.session)

        if not user.phone:
            raise BaseDomainException('user ha no atribute phone')

        request = self.waha_adapter.send_code_for_login_waha(
            user.session, user.phone
        )
        if not request:
            raise BaseDomainException('error from server')

        return RequestCodeOutDTO(code=request.get('code'))  # type: ignore
