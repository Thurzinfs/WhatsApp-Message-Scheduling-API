from dataclasses import dataclass


@dataclass
class PhoneNumberVO:
    value: str

    def __post_init__(self):
        if (len(self.value) > 13 and len(self.value) < 12) or '@c.us' not in self.value:
            self.value = f'{self.value}@c.us'
