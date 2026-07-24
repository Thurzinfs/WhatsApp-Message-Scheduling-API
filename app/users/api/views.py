import base64
from typing import List
from uuid import UUID

from ninja import Router
from pydantic import EmailStr

from app.users.api.bearer import AuthBearer
from app.users.api.schemas import (
    ContactOutSchema,
    LoginInSchema,
    LoginOutSchema,
    QrCodeOutSchema,
    RequestCodeOutSchema,
    UserInSchema,
    UserOutSchema,
)
from config.dependencies import container

from django.db.transaction import atomic


router = Router()

auth_router = Router()

contact_router = Router()


@router.post('/', response={201: UserOutSchema})
@atomic
def register_user(request, data: UserInSchema):
    dto = data.to_dto()

    use_case = container.users.register_user_use_case()

    user = use_case.execute(dto)

    return 201, UserOutSchema.from_domain(user)


@router.get('/email', response={200: UserOutSchema})
def response_user_by_email(request, email: EmailStr):
    use_case = container.users.response_user_by_email_use_case()

    user = use_case.execute(str(email))

    return 200, UserOutSchema.from_domain(user)


@router.get('/{id}', response={200: UserOutSchema})
def response_user(request, id: UUID):
    use_case = container.users.response_user_use_case()

    user = use_case.execute(id)

    return 200, UserOutSchema.from_domain(user)


@router.get(
    '/login/qr-code', response={200: QrCodeOutSchema}, auth=AuthBearer()
)
def login_qrcode_waha(request):
    use_case = container.users.login_qrcode_waha_use_case()

    qr_code = use_case.execute(request.auth.id)

    if qr_code is None:
        return QrCodeOutSchema(connected=True, qr_code_base64=None)

    encoded = base64.b64encode(qr_code).decode('utf-8')
    return QrCodeOutSchema(
        connected=False, qr_code_base64=f'data:image/png;base64,{encoded}'
    )


@router.get(
    '/login/request-code',
    response={200: RequestCodeOutSchema},
    auth=AuthBearer(),
)
def login_code_waha(request):
    use_case = container.users.login_code_waha_use_case()

    code = use_case.execute(request.auth.id)

    return 200, RequestCodeOutSchema.from_domain(code)


@router.delete('/{id}', response={200: UserOutSchema})
@atomic
def delete_user(request, id: UUID):
    use_case = container.users.deactive_user_use_case()

    user = use_case.execute(id)

    return 200, UserOutSchema.from_domain(user)


@router.patch('/{id}', response={200: UserOutSchema})
@atomic
def enable_permission_sync_contact(request, id: UUID):
    use_case = container.users.enable_sync_contacts_use_case()

    user = use_case.execute(id)

    return 200, UserOutSchema.from_domain(user)


@contact_router.get('/sync', response={200: None}, auth=AuthBearer())
@atomic
def sync_contacts(request):
    task = container.users.task_sync_adapter()

    task.sync(request.auth.id)
    return 200, None


@contact_router.get('/list/sync-contacts', response={200: List[ContactOutSchema]}, auth=AuthBearer())
def list_contacts_by_user(request):
    use_case = container.users.list_contacts_by_user_use_case()

    contacts = use_case.execute(request.auth.id)

    return 200, [
        ContactOutSchema.from_domain(contact)
        for contact in contacts
    ]


@contact_router.get('/id', response={200: ContactOutSchema})
def response_contact_by_id_router(request, id: UUID):
    use_case = container.users.response_contact_by_id()

    contact = use_case.execute(id)

    return 200, ContactOutSchema.from_domain(contact)


@contact_router.get('/', response={200: ContactOutSchema})
def response_contact_by_number(request, number: str):
    use_case = container.users.response_contact_by_number()

    contact = use_case.execute(number)

    return 200, ContactOutSchema.from_domain(contact)


@auth_router.post('/login', response={201: LoginOutSchema})
def login_user(request, data: LoginInSchema):
    dto = data.to_dto()

    use_case = container.users.login_use_case()

    user = use_case.execute(dto)

    return 201, LoginOutSchema.from_domain(user)


@auth_router.get('/me', response={200: UserOutSchema}, auth=AuthBearer())
def request_me(request):
    print(f'OBS: {request.auth.id}')
    return 200, UserOutSchema.from_domain(request.auth)
