from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext

def mailer(request):
    """Renders the mailer page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'mailer/mailer.html',
        context_instance = RequestContext(request,
        {
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )
