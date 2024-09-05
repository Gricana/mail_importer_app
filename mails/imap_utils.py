import email
import imaplib
from email.header import decode_header

from django.conf import settings

from .models import Email


async def get_emails(account, password, consumer):
    domain = account.split('@')[1]
    imap_server = settings.IMAP_SERVERS.get(domain)

    if not imap_server:
        await consumer.send_progress(0, 'Unsupported email provider')
        return

    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(account, password)
        mail.select('inbox')

        result, data = mail.search(None, 'ALL')
        mail_ids = data[0].split()
        total_mails = len(mail_ids)

        for idx, mail_id in enumerate(mail_ids):
            result, message_data = mail.fetch(mail_id, "(RFC822)")
            raw_email = message_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type in ['text/plain', 'text/html']:
                        body = part.get_payload(decode=True).decode('utf-8')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8')

            Email.objects.create(
                account=account,
                subject=subject,
                date_sent=msg.get('Date'),
                body=body,
                attachment=[]
            )

            progress = int((idx + 1) / total_mails * 100)
            await consumer.send_progress(progress, f"Загружено {idx + 1} из {total_mails} писем")

            await consumer.send_message({
                'subject': subject,
                'date_sent': msg['Date'],
                'body': body
            })

        mail.logout()
    except Exception as e:
        await consumer.send_progress(0, str(e))
