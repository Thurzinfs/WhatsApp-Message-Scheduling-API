from uuid import UUID

from app.message.domain.i_adapters import (
    ITaksSendMessageAdapter,
    IWahaMessageAdapter,
)

from app.message.infrastructure.tasks import send_message as task_send_message

import requests

from config import settings


class WahaMessageAdapter(IWahaMessageAdapter):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

        self.http = requests.Session()
        self.http.headers.update({'X-Api-Key': settings.WAHA_API_KEY})

    def send_message(self, number: str, message: str, session: str):
        try:
            response = self.http.post(
                url=f'{self.base_url}/api/sendText',
                json={
                    'chatId': f'{number}@c.us',
                    'text': message,
                    'session': session,
                },
            )
            print(f'[DEBUG] status={response.status_code} body={response.text}')

            response.raise_for_status()
        except requests.ConnectTimeout as e:
            raise e

    def create_session(self, session: str):
        try:
            response = self.http.post(
                url=f'{self.base_url}/api/sessions', json={'name': session}
            )
            response.raise_for_status()
        except requests.ConnectTimeout as e:
            raise e

    def start_session(self, session: str):
        try:
            response = self.http.post(
                url=f'{self.base_url}/api/sessions/{session}/start',
                json={'session': session},
            )
            response.raise_for_status()
        except requests.ConnectTimeout as e:
            raise e

    def get_session_status(self, session: str):
        try:
            response = self.http.get(
                url=f'{self.base_url}/api/sessions/{session}',
                json={'session': session},
            )
            if response.status_code == 404:
                return None
            return response.json().get('status')
        except requests.ConnectTimeout as e:
            raise e

    def get_login_qrcode(self, session: str):
        try:
            response = self.http.get(
                url=f'{self.base_url}/api/{session}/auth/qr',
                params={'format': 'image'},
            )
            response.raise_for_status()
            return response.content

        except requests.ConnectTimeout as e:
            raise e

    def send_code_for_login_waha(
        self, session: str, phone: str
    ) -> dict | None:
        try:
            response = self.http.post(
                url=f'{self.base_url}/api/{session}/auth/request-code',
                json={'phoneNumber': phone},
            )
            response.raise_for_status()
            return response.json()

        except requests.ConnectTimeout as e:
            raise e
        
    def delete_session(self, session: str):
        try:
            response = self.http.delete(
                url=f'{self.base_url}/api/sessions/{session}',
                json={
                    'session': session
                }
            )
            response.raise_for_status()

        except requests.ConnectTimeout as e:
            raise e


class TaskSendMessageAdapter(ITaksSendMessageAdapter):
    def send_message(self, id: UUID):
        task_send_message.delay(id)  # type: ignore
