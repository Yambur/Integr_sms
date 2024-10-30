# emails/urls.py
from django.urls import path
from . import views
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view, name='email_list'),
    path('api/', views.email_list_api, name='message_list_api'),
    path('fetch/<int:account_id>/', views.fetch_emails_view, name='fetch_emails'),
]