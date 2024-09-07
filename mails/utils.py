import os
from datetime import datetime
from email.header import decode_header

from bs4 import BeautifulSoup
from dateutil import parser
from django.conf import settings
from django.core.serializers import serialize

from mails.models import Email


def parse_email_date(date_str: str) -> datetime:
    """
    Parses a date string in various formats into a datetime object.

    Parameters:
    date_str (str): The date string to be parsed.

    Returns:
    datetime.datetime: The parsed date as a datetime object.
    """
    date_obj = parser.parse(date_str)
    return date_obj


async def parse_body(msg) -> str:
    """
    Asynchronously parses the body of an email message.

    The function handles both multipart and non-multipart email messages.
    For multipart messages, it searches for 'text/plain' and 'text/html' parts.
    If a 'text/plain' part is found, it sets the body to the decoded payload.
    If a 'text/html' part is found, it extracts the text from the HTML using BeautifulSoup.
    For non-multipart messages, it sets the body to the decoded payload.

    Parameters:
    msg (email.message.Message): The email message to parse.

    Returns:
    str: The parsed email body.
    """
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                body = part.get_payload(decode=True).decode('utf-8')
                break
            elif content_type == 'text/html':
                html = part.get_payload(decode=True).decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')
                body = soup.get_text()
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8')
    return body


def decode_filename(filename: str) -> str:
    """
    Decodes a filename from its encoded form using the email.header.decode_header function.

    The function handles filenames that may be encoded using various character sets.

    Parameters:
    filename (str): The encoded filename to be decoded.

    Returns:
    str: The decoded filename.
    """
    decoded_header = decode_header(filename)
    decoded_filename = ''.join(
        [str(part[0], part[1] or 'utf-8') if isinstance(part[0], bytes) else part[0] for part in decoded_header])
    return decoded_filename


async def save_attachment(part) -> str | None:
    """
    Asynchronously saves an email attachment to the specified media directory.

    Parameters:
    part (email.message.Message): The email part containing the attachment.

    Returns:
    str: The filename of the saved attachment, or None if the filename is empty.
    """
    filename = decode_filename(part.get_filename())
    if filename:
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        with open(filepath, 'wb') as f:
            f.write(part.get_payload(decode=True))
        return filename
    return None


async def serialize_email(email_obj: Email) -> str:
    """
    Asynchronously serializes an email object into JSON format.

    The serialized JSON fields: 'subject', 'date_sent', 'date_received', 'body', and 'attachments'.

    Parameters:
    email_obj (Email): The email object to be serialized.

    Returns:
    str: The serialized email object in JSON format.
    """
    serialized_email = serialize(
        'json',
        [email_obj],
        fields=['subject', 'date_sent', 'date_received', 'body', 'attachments']
    )
    return serialized_email
