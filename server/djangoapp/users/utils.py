from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site

from users.tokens import generate_token
from app import settings


def send_confirmation_email(request, user):
    """Отправка письма с подтверждением email."""
    current_site = get_current_site(request)
    mail_subject = 'Подтвердите ваш email'
    message = render_to_string('users/emails/email_confirmation.html', {
        'user': user,
        'name': user.first_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
    })

    email = EmailMessage(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    return email.send(fail_silently=False)