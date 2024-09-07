from asgiref.sync import sync_to_async
from django.db import models

from account.models import Account


class Email(models.Model):
    """
    This class represents an Email model in a Django application.

    Attributes:
    account (models.ForeignKey): The account associated with the email.
    uid (models.IntegerField): The unique identifier of the email.
    subject (models.CharField): The subject of the email.
    date_sent (models.DateTimeField): The date and time when the email was sent.
    date_received (models.DateTimeField): The date and time when the email was received.
    body (models.TextField): The content of the email.
    attachments (models.JSONField): The attachments associated with the email.

    Methods:
    __str__(): Returns a string representation of the email.
    get_last_email_uid(cls, account): A class method that retrieves the unique identifier of the last email for a given account.
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='emails')
    uid = models.IntegerField()
    subject = models.CharField(max_length=255, null=True)
    date_sent = models.DateTimeField()
    date_received = models.DateTimeField()
    body = models.TextField(null=True)
    attachments = models.JSONField(default=list)

    def __str__(self):
        return f"{self.account} получил {self.date_received} {self.subject}"

    @classmethod
    @sync_to_async
    def get_last_email_uid(cls, account):
        """
        Retrieves the unique identifier of the last email for a given account.

        Parameters:
        account (Account): The account for which to retrieve the last email's unique identifier.

        Returns:
        int: The unique identifier of the last email for the given account. If no email exists, returns None.
        """
        last_email = cls.objects.filter(account=account).order_by('-uid').first()
        return last_email.uid if last_email else None

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        unique_together = ('account', 'uid')
