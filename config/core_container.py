from dependency_injector import containers, providers

from app.message.infrastructure.adapters import WahaMessageAdapter
from app.message.infrastructure.service import HashService
from app.users.infrastructure.repository import UserRepository


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    waha_adapter = providers.Singleton(
        WahaMessageAdapter, base_url=config.waha.base_url
    )

    hash_service = providers.Singleton(HashService)

    user_repo = providers.Factory(UserRepository)
