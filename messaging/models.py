from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    content = models.TextField()
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"

class BroadcastMessage(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_superuser': True}
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Broadcast by {self.sender.username}"