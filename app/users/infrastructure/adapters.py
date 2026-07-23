from uuid import UUID

from app.users.domain.I_adapter import IContactsSyncTaskAdapter
from app.users.infrastructure.task import sync_contacts


class ContactsSyncTaskAdapter(IContactsSyncTaskAdapter):
    def sync(self, id: UUID):
        sync_contacts.delay(id)  # type: ignore
