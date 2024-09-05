from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def mails(request):
    return render(request, 'mail/mails.html')
