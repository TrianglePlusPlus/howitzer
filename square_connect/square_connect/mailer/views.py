from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from mailer.models import MailingList, Person
from mailer.forms import PersonForm
from app.models import Service
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.contrib import messages

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
                # add to mailing list
                mailing_list = form.cleaned_data['mailing_list']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                send_mail(
                    "Mailing List Notification",
                    "Hello " + first_name + " " + last_name + "! You were added to the " + mailing_list.service.name + " mailing list.",
                    "reports@thecorp.org",
                    [email],
                    fail_silently = False,
                )
                form.save()
                messages.success(request, first_name + ' ' + last_name + ' was successfully added to the ' + mailing_list.service.name + ' mailing list.') 
                form = PersonForm()

        else:
            # remove from mailing list
            Person.objects.get(pk=request.POST.get('person')).delete()
            form = PersonForm()
            messages.success(request, 'Delete sucessful.')
    else:
        form = PersonForm()

    mailing_lists = MailingList.objects.all()

    return render(
        request,
        'mailer/mailer.html',
        {
            'mailing_lists': mailing_lists,
            'title':'Report Viewer',
            'year':'Remember never give up.',
            'form': form,
        }
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
