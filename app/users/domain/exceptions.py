from core.exceptions import BaseDomainException


class UserNotFoundException(BaseDomainException):
    pass


class ContactNotFoundException(BaseDomainException):
    pass


class ConfigurationUserNotEnabledException(BaseDomainException):
    pass
