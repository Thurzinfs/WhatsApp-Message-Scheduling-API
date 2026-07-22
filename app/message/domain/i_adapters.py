from abc import ABC, abstractmethod


class IWahaMessageAdapter(ABC):
    @abstractmethod
    def send_message(self, number: str, message: str, session: str):
        ...

    @abstractmethod
    def create_session(self, session: str):
        ...

    @abstractmethod
    def start_session(self, session: str):
        ...

    @abstractmethod
    def get_session_status(self, session: str):
        ...

    @abstractmethod
    def get_login_qrcode(self, session: str):
        ...

    @abstractmethod
    def send_code_for_login_waha(
        self, session: str, phone: str
    ) -> dict | None:
        ...

    @abstractmethod
    def delete_session(self, session: str):
        ...


class ITaksSendMessageAdapter(ABC):
    @abstractmethod
    def send_message(self, id):
        ...
