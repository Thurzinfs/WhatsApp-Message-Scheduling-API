from uuid import uuid4

from django.db import models


class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    token = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    class Meta:
        db_table = 'refresh_token'
