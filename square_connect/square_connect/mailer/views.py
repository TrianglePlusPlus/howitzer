from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from mailer.models import MailingList, Person
from mailer.forms import MailerPersonForm
from app.models import Service
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail

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
            form = MailerPersonForm(request.POST)
            if form.is_valid():
                # add to mailing list
                form.save()
                mailing_list = form.cleaned_data['mailing_list']
                service = mailing_list.service
                service_name = service.name
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                discount = form.cleaned_data['discount']
                discount_str = ''
                if discount != 'all':
                    discount_str = ' Your results will be filtered for the ' + discount + ' discount.'
                send_mail(
                    "Mailing List Notification",
                    "Hello " + first_name + " " + last_name + "! You were added to the mailing list of " + service_name + "." + discount_str,
                    "reports@thecorp.org",
                    [email],
                    fail_silently=False
                )

                form = MailerPersonForm()
        else:
            # remove from mailing list
            Person.objects.get(pk=request.POST.get('person')).delete()
            form = MailerPersonForm()
    else:
        form = MailerPersonForm()

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
