from dependency_injector import containers, providers

from app.authentication.api.dependencies import AuthContainer
from app.message.api.dependencies import MessageContainer
from app.users.api.dependencies import UserContainer
from config.core_container import CoreContainer


class AppContainer(containers.DeclarativeContainer):
    core = providers.Container(CoreContainer)

    auth = providers.Container(AuthContainer, core=core)

    messages = providers.Container(MessageContainer, core=core)

    users = providers.Container(UserContainer, core=core)
