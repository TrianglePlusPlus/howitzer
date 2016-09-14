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

    # Check if they are adding a Person
    if request.POST.get('first_name', False):
        # They are adding a Person
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
    else:
        form = PersonForm()

    people = Person.objects.all()
    mailing_lists = MailingList.objects.all()

    return render(
        request,
        'mailer/mailer.html',
        context_instance = RequestContext(request,
        {
            'mailing_lists': mailing_lists,
            'people': people,
            'title':'Report Viewer',
            'year':'Remember never give up.',
            'form': form,
        })
    )
