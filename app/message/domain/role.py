from django.db.models import TextChoices


class StatusMessage(TextChoices):
    sent = 'sent', 'SENT'
    pending = 'pending', 'PENDING'
    process = 'process', 'PROCESS'
