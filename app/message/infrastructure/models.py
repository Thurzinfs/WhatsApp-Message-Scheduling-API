from django.db import models

from app.message.domain.role import StatusMessage


class Message(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, null=False)
    message = models.CharField(max_length=290)
    scheduled_at = models.DateTimeField(null=True)
    number = models.CharField(max_length=60)
    session = models.CharField(max_length=100, null=True)
    status = models.CharField(
        max_length=45, choices=StatusMessage, default=StatusMessage.pending
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
