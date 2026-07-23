from uuid import uuid4

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=190)
    email = models.EmailField()
    password = models.CharField(max_length=120)

    phone = models.CharField(max_length=180, null=True)

    connected = models.BooleanField(default=False)

    session = models.CharField(max_length=100)
    session_started = models.BooleanField(default=False)

    access_contacts = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    contact_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=130)
    number = models.CharField(max_length=180, unique=True)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contacts'


class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    token = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    class Meta:
        db_table = 'refresh_token'
