from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from mailer.models import MailingList, Person
from mailer.forms import PersonForm

@login_required
def mailer(request):
    """Renders the mailer page.
    request.POST dictionary keys:
        mailing_list
        first_name
        last_name
        email"""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            form = PersonForm()
    else:
        form = PersonForm()

    mailing_lists = MailingList.objects.all()

    return render(
        request,
        'mailer/mailer.html',
        context_instance = RequestContext(request,
        {
            'mailing_lists': mailing_lists,
            'title':'Report Viewer',
            'year':'Remember never give up.',
            'form': form,
        })
    )
