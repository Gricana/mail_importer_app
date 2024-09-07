import asyncio
import email
import imaplib
import json
from email.header import decode_header

from django.conf import settings

from .models import Email
from .utils import parse_email_date, parse_body, save_attachment, serialize_email


async def get_emails(account, consumer):
    """
    Asynchronously fetches emails from a specified account using IMAP.

    Parameters:
    - account: An instance of the Account model representing the email account.
    - consumer: An instance of the consumer object
                that handles progress updates and message sending.

    Returns:
    - None

    Raises:
    - imaplib.IMAP4_SSL.error: Error connecting to the IMAP server
                               or performing IMAP operations.
    """
    domain = account.email.split('@')[1]
    imap_server = settings.IMAP_SERVERS.get(domain)

    if not imap_server:
        await consumer.send_progress(0, 'Unsupported email provider')
        return

    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(account.email, account.get_password())
        mail.select('inbox')

        last_uid = await Email.get_last_email_uid(account=account)

        search_criteria = f"(UID {int(last_uid) + 1}:*)" if last_uid else "ALL"
        result, data = mail.uid('SEARCH', search_criteria)
        mail_uids = data[0].split()
        total_mails = len(mail_uids)

        if total_mails == 1:
            await consumer.send_progress(100, 'No new messages')
            mail.close()
            mail.logout()
            return

        created_emails = []

        for idx, mail_uid in enumerate(mail_uids):
            await consumer.send_progress(0, f"Чтение сообщения {idx + 1} из {total_mails}")

            if last_uid and int(mail_uid) <= last_uid:
                break

            result, message_data = mail.uid('fetch', mail_uid, "(RFC822)")
            raw_email = message_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            body = await parse_body(msg)

            attachments = []
            for part in msg.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = await save_attachment(part)
                    if filename:
                        attachments.append(filename)

            email_dict = dict(
                account=account,
                uid=mail_uid,
                subject=subject,
                date_sent=parse_email_date(msg.get('Date')),
                date_received=parse_email_date(
                    msg.get('Received').split(';')[-1].strip()
                ),
                body=body,
                attachments=attachments
            )
            email_obj = await Email.objects.acreate(**email_dict)
            created_emails.append(email_obj)

            progress = int((idx + 1) / total_mails * 100)
            await consumer.send_progress(
                progress,
                f"Проверено {idx + 1} из {total_mails} писем"
            )

        for idx in range(total_mails - 1, -1, -1):
            await consumer.send_progress(
                int((total_mails - idx) / total_mails * 100),
                f"Обратный отсчет: осталось {idx} писем"
            )

            # To visually check that the progress update is correct
            # await asyncio.sleep(3)

            serialized_email = await serialize_email(created_emails[idx])
            await consumer.send_message(json.dumps(
                json.loads(serialized_email)[0]['fields']
            ))

        mail.close()
        mail.logout()
    except imaplib.IMAP4_SSL.error as e:
        await consumer.send_progress(0, str(e))
