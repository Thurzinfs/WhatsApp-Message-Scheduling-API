from dataclasses import dataclass

from core.exceptions import BaseDomainException


@dataclass
class PhoneNumberVO:
    value: str

    def __post_init__(self):
        if len(self.value) > 13 or len(self.value) < 12:
            raise BaseDomainException('phone number is invalid')
    