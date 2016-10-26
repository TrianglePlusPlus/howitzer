from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from mailer.models import MailingList, Person
from mailer.forms import PersonForm
from app.models import Service
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

import json

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
        pass
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

@csrf_exempt
def add_emp(request):

    if request.method == "POST":

        mailing_list_num = request.POST.get('mailing_list', None)
        mailing_list = MailingList.objects.get(id=mailing_list_num)
        service = mailing_list.service
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        person = Person.objects.create_person(mailing_list,first_name,last_name,email)
        person.save()

        response_data = {}
        response_data['result'] = 'Successful Submit!'
        response_data['person_id'] = person.id
        response_data['person_first_name'] = person.first_name
        response_data['person_last_name'] = person.last_name
        response_data['person_email'] = person.email
        response_data['person_service'] = service.name
        response_data['person_service_id'] = service.merchant_id

        send_mail(
            "Mailing List Notification",
            "Hello " + first_name + " " + last_name + "! You were added to the " + service.name + " mailing list.",
            "reports@thecorp.org",
            [email],
            fail_silently = False,
        )

        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
        
    else:
        return HttpResponse(
            json.dumps({"POST method failed": "we have no data for you"}),
            content_type = "application/json"
        )

@csrf_exempt
def delete_emp(request):
    
    if request.method == "POST":  
        
        person_id = request.POST.get('person', None)
        print(person_id)
        person = Person.objects.get(id=person_id)
        
        response_data = {}
        response_data['result'] = 'Successful Delete!'
        response_data['person_id'] = person.id
        response_data['person_first_name'] = person.first_name
        response_data['person_last_name'] = person.last_name
        response_data['person_email'] = person.email
        response_data['person_service'] = person.mailing_list.service.name
        response_data['person_service_id'] = person.mailing_list.service.merchant_id


        person.delete()

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
       return HttpResponse(
            json.dumps({"POST method failed": "we have no data for you"}),
            content_type="application/json"
        )

