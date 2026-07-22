class BaseDomainException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class FieldRequiredException(BaseDomainException):
    pass


class ConflictFieldException(BaseDomainException):
    pass
