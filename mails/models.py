from django.db import models
from account.models import Account
from django.utils import timezone


class Email(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='emails')
    subject = models.CharField(max_length=255)
    date_sent = models.DateTimeField()
    date_received = models.DateTimeField(default=timezone.now)
    body = models.TextField(blank=True)
    attachment = models.JSONField(default=list)

    def __str__(self):
        return f"{self.account} получил {self.date_received} {self.subject}"

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
