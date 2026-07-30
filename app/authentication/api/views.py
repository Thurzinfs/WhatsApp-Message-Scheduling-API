from django.http import HttpRequest, HttpResponse
from ninja import Router

from app.authentication.api.schemas import LoginInSchema
from app.authentication.api.cookie import AuthCookie
from app.users.api.schemas import UserOutSchema
from config import settings

from config.dependencies import container


auth_router = Router()


@auth_router.post('/login', response={201: str})
def login_user(request, data: LoginInSchema, response: HttpResponse):
    dto = data.to_dto()

    use_case = container.auth.login_use_case()

    token = use_case.execute(dto)

    response.set_cookie(
        'access_token',
        value=token.access_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age= 60 * settings.JWT_EXP_MINUTES
    )

    response.set_cookie(
        'refresh_token',
        value=token.refresh_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=60 * 60 * 24 * settings.JWT_EXP_DAYS
    )

    return 201, 'User successfully logged in'


@auth_router.post('/refresh', response={200: str})
def refresh_token_user(request: HttpRequest, response: HttpResponse):
    raw_refresh = request.COOKIES.get('refresh_token')

    use_case = container.auth.refresh_token_use_case()

    access = use_case.execute(raw_refresh)

    response.set_cookie(
        'access_token',
        value=access,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=60 * settings.JWT_EXP_MINUTES
    )
    return 200, "Refresh token successfully renewed"


@auth_router.delete('/logout', response={200: str})
def logout_user(response: HttpResponse):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return 200, "User successfully logged out"


@auth_router.get('/me', response={200: UserOutSchema}, auth=AuthCookie())
def request_me(request):
    return 200, UserOutSchema.from_domain(request.auth)
