from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from mailer.models import Person, Subscription
from mailer.forms import PersonForm, SubscriptionForm
from app.models import Service
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings

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
        # if it's a PersonForm
        if request.POST.get('person') == None:
            person_form = PersonForm(request.POST)
            if person_form.is_valid():
                # add to mailing list
                person_form.save()

                person_form = PersonForm()
                subscription_form = SubscriptionForm()
        # if it's a person deletion
        elif request.POST.get('service') == None and request.POST.get('subscription') == None:
            # remove from mailing list
            Person.objects.get(pk=request.POST.get('person')).delete()

            person_form = PersonForm()
            subscription_form = SubscriptionForm()
        # if it's a SubscriptionForm
        elif request.POST.get('subscription') == None:
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                # add subscription to person
                sub = subscription_form.save()
                person = Person.objects.get(pk=request.POST.get('person'))
                person.subscriptions.add(sub)

                # notification email
                discount_str = ''
                if sub.discount != 'all':
                    discount_str = ' Your results will be filtered for the ' + sub.discount + ' discount.'
                send_mail(
                    "Mailing List Notification",
                    "Hello " + str(person) + "! You were added to the mailing list of " + settings.SERVICE_NAMES[sub.service] + "." + discount_str,
                    settings.EMAIL_HOST_USER,
                    [person.email],
                    fail_silently=False
                )

                person_form = PersonForm()
                subscription_form = SubscriptionForm()
        # if it's a subscription deletion
        else:
            # remove subscription from person
            Person.objects.get(pk=request.POST.get('person')).subscriptions.remove(Subscription.objects.get(pk=request.POST.get('subscription')))

            person_form = PersonForm()
            subscription_form = SubscriptionForm()
    else:
        person_form = PersonForm()
        subscription_form = SubscriptionForm()

    persons = Person.objects.all()

    return render(
        request,
        'mailer/mailer.html',
        {
            'persons': persons,
            'title':'Report Viewer',
            'year':'Remember never give up.',
            'person_form': person_form,
            'subscription_form': subscription_form,
        }
    )
