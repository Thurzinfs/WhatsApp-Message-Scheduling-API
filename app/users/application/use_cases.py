from uuid import UUID

from app.message.domain.i_adapters import IWahaMessageAdapter
from app.message.domain.servicies import IHashService
from app.users.application.dto import (
    ContactOutDTO,
    LoginInDTO,
    LoginOutDTO,
    RequestCodeOutDTO,
    UserInDTO,
    UserOutDTO,
)
from app.users.domain.I_adapter import IContactsSyncTaskAdapter
from app.users.domain.entities import UserEntity
from app.users.domain.exceptions import ContactNotFoundException, UserNotFoundException
from app.users.domain.repositories import (
    IContactsRepository,
    IRefreshTokenRepository,
    IUserRepository,
)
from app.users.domain.servicies import IFilterContactsService, ITokenService
from app.users.domain.value_objects import PhoneNumberVO
from core.exceptions import BaseDomainException


class EnableSyncContactsUseCase:
    def __init__(self, user_repo: IUserRepository, task_sync_adapter: IContactsSyncTaskAdapter) -> None:
        self.user_repo = user_repo
        self.task_sync_adapter = task_sync_adapter

    def execute(self, id: UUID):
        user = self.user_repo.find_by_id(id)
        if not user:
            raise UserNotFoundException('user not found')

        self.task_sync_adapter.sync(user.id)

        user.change_permissions(access_contacts=True)
        self.user_repo.save(user)

        return UserOutDTO.from_domain(user)


class SyncContactsUserUseCase:
    def __init__(self, user_repo: IUserRepository, waha_adapter: IWahaMessageAdapter, filter_service: IFilterContactsService, contact_repo: IContactsRepository) -> None:
        self.user_repo = user_repo
        self.waha_adapter = waha_adapter
        self.filter_service = filter_service
        self.contact_repo = contact_repo

    def execute(self, id: UUID):
        user = self.user_repo.find_by_id(id)
        if not user:
            raise UserNotFoundException('user not found')

        if user.access_contacts is False:
            raise BaseDomainException('user not enabled to sync contacts')

        contacts_list = self.waha_adapter.list_contacts(user.session)
        print(f"[DEBUG] use case sync: {contacts_list}")

        contacts = self.filter_service.list_contacts(
            contacts_list=contacts_list,
            id=user.id
        )
        print(f"[DEBUG] use case sync filter: {contacts}")

        for contact in contacts:
            if self.contact_repo.verify_by_id_waha(contact.contact_id) is not None:
                continue

            self.contact_repo.save(contact)


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

    def execute(self, token: str):
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


class ListContactsByUserUseCase:
    def __init__(self, contact_repo: IContactsRepository) -> None:
        self.contact_repo = contact_repo

    def execute(self, id: UUID):
        contacts = self.contact_repo.list_by_user(id)
        if not contacts:
            return []

        return [
            ContactOutDTO.from_domain(contact)
            for contact in contacts
        ]
    

class ResponseContactByIDUseCase:
    def __init__(self, contact_repo: IContactsRepository) -> None:
        self.contact_repo = contact_repo

    def execute(self, id: UUID):
        contact = self.contact_repo.find_by_id(id)
        if not contact:
            raise ContactNotFoundException('contact not found')

        return ContactOutDTO.from_domain(contact)


class ResponsenContactByNumberUseCase:
    def __init__(self, contact_repo: IContactsRepository) -> None:
        self.contact_repo = contact_repo

    def execute(self, number: str):
        contact = self.contact_repo.find_by_number(PhoneNumberVO(number))
        if not contact:
            raise ContactNotFoundException('contact not found')

        return ContactOutDTO.from_domain(contact)
