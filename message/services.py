import imaplib
import email
from message.models import EmailMessage, EmailAccount


def fetch_emails(account_id):
    account = EmailAccount.objects.get(id=account_id)
    # Подключение к серверу электронной почты
    mail = imaplib.IMAP4_SSL('imap.yandex.com' if account.provider == 'yandex' else 'imap.gmail.com')
    mail.login(account.email, account.password)
    mail.select('inbox')

    # Получение электронных писем
    status, messages = mail.search(None, 'ALL')
    messages = messages.split()

    for num in messages:
        status, msg = mail.fetch(num, '(RFC822)')
        raw_message = msg
        message = email.message_from_bytes(raw_message)

        # Извлечение необходимой информации
        subject = message['Subject']
        sent_date = message['Date']
        received_date = message['Date']
        body = ''
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))

                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass

        # Сохранение электронного письма
        EmailMessage.objects.create(
            subject=subject,
            sent_date=sent_date,
            received_date=received_date,
            body=body,
            account=account
        )

    mail.close()
    mail.logout()
