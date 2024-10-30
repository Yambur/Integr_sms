from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView

from .models import EmailMessage
from .services import fetch_emails


class IndexView(TemplateView):
    template_name = 'message/index.html'
    extra_context = {
        'title': 'Сообщения - Главная'
    }


def email_list_api(request):
    emails = EmailMessage.objects.all().values()
    return JsonResponse(list(emails), safe=False)


def fetch_emails_view(request, account_id):
    fetch_emails(account_id)
    return JsonResponse({'message': 'Электронные письма обрабатываются'})
