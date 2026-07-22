from dependency_injector import containers, providers

from app.message.infrastructure.adapters import WahaMessageAdapter
from app.message.infrastructure.service import HashService


class CoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    waha_adapter = providers.Singleton(
        WahaMessageAdapter, base_url=config.waha.base_url
    )

    hash_service = providers.Singleton(HashService)
