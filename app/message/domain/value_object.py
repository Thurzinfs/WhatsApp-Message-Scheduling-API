from dataclasses import dataclass
from datetime import datetime

from django.utils import timezone


@dataclass(frozen=True)
class ScheduledAtTime:
    value: datetime

    def __post_init__(self):
        if isinstance(self.value, (int, float)):
            object.__setattr__(
                self,
                'value',
                datetime.fromtimestamp(self.value, tz=timezone.utc),
            )
        elif isinstance(self.value, str):
            object.__setattr__(
                self, 'value', datetime.fromisoformat(self.value)
            )
