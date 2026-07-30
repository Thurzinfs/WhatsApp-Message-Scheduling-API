from typing import List
from uuid import UUID

from ninja import Router

from app.message.api.schemas import MessageInSchema, MessageOutSchema

from app.message.api.dependencies import MessageContainer

from django.db.transaction import atomic

from app.authentication.api.cookie import AuthCookie
from config.dependencies import container

router = Router()


@router.post('/', response={201: MessageOutSchema}, auth=AuthCookie())
@atomic
def register_message(request, data: MessageInSchema):
    dto = data.to_dto()

    use_case = container.messages.register_message_use_case()

    message = use_case.execute(dto, request.auth.id)

    return 201, MessageOutSchema.from_domain(message)


@router.get('/list', response={200: List[MessageOutSchema]}, auth=AuthCookie())
def list_messages(request, number: str):
    use_case = container.messages.list_messages_by_number()

    messages = use_case.execute(number)

    return 200, [MessageOutSchema.from_domain(message) for message in messages]


@router.get('/{id}', response={200: MessageOutSchema}, auth=AuthCookie())
def response_message_by_id(request, id: UUID):
    use_case = container.messages.response_message_by_id()

    message = use_case.execute(id)

    return 200, MessageOutSchema.from_domain(message)
