from django.dispatch import receiver, Signal
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings
from user import constants as cs
from .models import User, NewSignup


new_signup = Signal(providing_args=['user'])

signup_denied = Signal(providing_args=['user'])

signup_approved = Signal(providing_args=['user'])


@receiver(new_signup)
def email_new_signup(sender, **kwargs):
    user = kwargs['user']
    admins = User.objects.filter(is_superuser=True).values('email')
    unapproved_count = User.objects.filter(profile__is_approved=False).count()
    rendered = render_to_string('emails/signup_admin.html', {
        'user': user,
        'user_type': cs.USER_ROLE_CHOICES[user.role - 1][1],
        'unapproved_count': unapproved_count,
        'opts': NewSignup._meta,
        'hostname': settings.HOST_NAME
    })

    for admin in admins:
        send_mail(
            _('New User Signup in Varuna'),
            None,
            settings.DEFAULT_FROM_EMAIL,
            [admin['email']],
            html_message=rendered,
            fail_silently=True
        )
    
    rendered = render_to_string('emails/signup_user.html', { 'user': user })

    send_mail(
        _('Signup request to Varuna has been sent'),
        None,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=rendered,
        fail_silently=True
    )


@receiver(signup_approved)
def email_signup_approval(sender, **kwargs):
    user = kwargs['user']
    rendered = render_to_string('emails/signup_approved.html', {
        'user': user,
        'appname': settings.APP_NAME
    })

    send_mail(
        _('Varuna Greetings'),
        None,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=rendered,
        fail_silently=True
    )


@receiver(signup_denied)
def email_signup_denial(sender, **kwargs):
    user = kwargs['user']
    rendered = render_to_string('emails/signup_denied.html', { 'user': user })

    send_mail(
        _('Sorry, Your signup request to Varuna has been disapproved'),
        None,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=rendered,
        fail_silently=True
    )
