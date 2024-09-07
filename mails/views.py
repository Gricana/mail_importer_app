from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Email


@login_required
def mails(request):
    """
    This function retrieves and displays a list of emails for the logged-in user.
    """
    emails = Email.objects.filter(account=request.user)
    return render(request, 'mail/mails.html', {'emails': emails})
