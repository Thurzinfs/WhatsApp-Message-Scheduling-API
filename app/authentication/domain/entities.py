from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from core.exceptions import BaseDomainException


@dataclass
class RefreshTokenEntity:
    id: UUID = field(default_factory=uuid4)
    token: str = field(default='')
    revoked: bool = field(default=False)
    user: UUID | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    expire_at: datetime | None = field(default=None)

    def revoked_token(self):
        if self.revoked:
            raise BaseDomainException('token already revoked')

        self.revoked = True

    def is_valid(self) -> bool:
        if not self.expire_at:
            return False
        return not self.revoked and datetime.now() < self.expire_at
