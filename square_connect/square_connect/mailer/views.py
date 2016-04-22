from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from mailer.models import MailingList, Person

def mailer(request):
    """Renders the mailer page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'mailer/mailer.html',
        context_instance = RequestContext(request,
        {
            'people': Person.objects.all(),
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )
