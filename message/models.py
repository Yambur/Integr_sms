from django.db import models


class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    provider = models.CharField(max_length=50, choices=[
        ('yandex', 'Yandex'),
        ('gmail', 'Gmail'),
        ('mailru', 'Mail.ru'),
    ])


class EmailMessage(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    body = models.TextField()
    attachments = models.FileField(upload_to='email_attachments/', blank=True, null=True)
    account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)

    class Meta:
        ordering = ('received_date',)

    def __str__(self):
        return self.subject
