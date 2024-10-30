import imaplib
import email


def fetch_emails():
    # Пример для яндекс почты, необходимо адаптировать для других провайдеров
    mail = imaplib.IMAP4_SSL('imap.yandex.ru')
    mail.login('your_email@yandex.ru', 'your_password')
    mail.select('inbox')
    status, messages = mail.search(None, 'ALL')
    messages = messages.split()
    emails = []
    for num in messages:
        status, msg = mail.fetch(num, '(RFC822)')
        raw_message = msg
        raw_email_string = raw_message.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        email_data = {
            'subject': email_message['Subject'],
            'sent_date': email_message['Date'],
            'body': '',
            'attachments': []
        }
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))

                try:
                    body = part.get_payload(decode=True).decode()
                    email_data['body'] = body
                except:
                    pass

                if content_type == 'application/octet-stream' and 'attachment' in content_disposition:
                    filename = content_disposition.split(';').split('=').strip('"')
                    attachment = part.get_payload(decode=True)
                    email_data['attachments'].append({'file': attachment, 'filename': filename})
        else:
            email_data['body'] = email_message.get_payload(decode=True).decode()

        emails.append(email_data)
    return emails
