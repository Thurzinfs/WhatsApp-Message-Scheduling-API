from ninja import NinjaAPI

from app.message.api.views import router as router_messages

from app.users.api.views import router as router_users, auth_router


api = NinjaAPI(title='Scheduled Messages for WhatsApp', docs_url='/docs/')

api.add_router('/auth', auth_router, tags=['Auth'])
api.add_router('/users', router_users, tags=['User'])
api.add_router('/message', router_messages, tags=['Message'])
