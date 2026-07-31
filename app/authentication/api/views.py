from django.http import HttpRequest, HttpResponse
from ninja import Router

from app.authentication.api.schemas import LoginInSchema, LoginOutSchema
from app.authentication.api.bearer import AuthBearer
from app.users.api.schemas import UserOutSchema

from config.dependencies import container


auth_router = Router()


@auth_router.post('/login', response={200: LoginOutSchema})
def login_user(request, data: LoginInSchema):
    dto = data.to_dto()

    use_case = container.auth.login_use_case()

    token = use_case.execute(dto)
    return LoginOutSchema.from_domain(token)


@auth_router.post('/refresh', response={200: str})
def refresh_token_user(request: HttpRequest):
    raw_refresh = request.COOKIES.get('refresh_token')

    use_case = container.auth.refresh_token_use_case()

    access = use_case.execute(raw_refresh)

    return 200, str(access)


@auth_router.get('/me', response={200: UserOutSchema}, auth=AuthBearer())
def request_me(request):
    print(f'EU: {request.auth.id}')
    return 200, UserOutSchema.from_domain(request.auth)
