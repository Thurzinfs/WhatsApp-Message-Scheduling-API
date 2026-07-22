from django.contrib import admin

from app.message.infrastructure.models import Message

admin.site.register(Message)
