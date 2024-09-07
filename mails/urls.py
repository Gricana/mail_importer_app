from django.urls import path

from .views import mails

urlpatterns = [
    path('', mails, name='mails'),
]
