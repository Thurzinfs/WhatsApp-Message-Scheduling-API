from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from app.users.domain.value_objects import PhoneNumberVO
from core.exceptions import BaseDomainException, FieldRequiredException


@dataclass
class UserEntity:
    id: UUID = field(default_factory=uuid4)
    name: str = field(default='')
    email: str = field(default='')
    password: str = field(default='')
    phone: str | None = field(default=None)
    connected: bool = field(default=False)
    session: str = field(default='')
    session_started: bool = field(default=False)
    access_contacts: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    def __post_init__(self):
        self.session = f'session_{self.id}'

    def delete(self):
        self.deleted_at = datetime.now()

    def change_connection_status(self, status: bool):
        self.connected = status

    def change_session_status(self, status: bool):
        self.session_started = status

    def change_permissions(self, access_contacts: bool):
        self.access_contacts = access_contacts


@dataclass
class ContactEntity:
    id: UUID = field(default_factory=uuid4)
    contact_id: str = field(default='')
    name: str = field(default='')
    number: str = field(default='')
    user: UUID | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)

    def change_name(self, name: str):
        if not name: 
            raise FieldRequiredException("name is required")

        self.name = name
