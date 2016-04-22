from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from mailer.models import MailingList, Person

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
        mailing_list = request.POST.get('mailing_list', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)

        p = Person(mailing_list=mailing_list, first_name=first_name, last_name=last_name, email=email)
        p.save()

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
        })
    )
