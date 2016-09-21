from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from mailer.models import MailingList, Person
from mailer.forms import PersonForm
from django.contrib.admin.views.decorators import staff_member_required

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
        if request.POST.get('person') == None:
            form = PersonForm(request.POST)
            if form.is_valid():
                form.save()
                form = PersonForm()
        else:
            Person.objects.get(pk=request.POST.get('person')).delete()
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

@staff_member_required
def mailer_admin(request, retcode=None):
    # if retcode:
    #     return render(
    #         request,
    #         'common/rt_update.html',
    #         context = RequestContext(request,
    #         {
    #             'retcode':retcode,
    #         })
    #     )
    # else:
    return render(
        request,
        'mailer/mailer_admin.html'
    )