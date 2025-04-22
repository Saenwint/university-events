from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

from app import settings


def send_ticket_email(request, user, event, ticket):
    """
    Отправка письма с билетом на мероприятие.
    """
    context = {
        'user': user,
        'event': event,
        'ticket': ticket,
        'unique_code': ticket.generate_qr_data(),
    }
    html_message = render_to_string('events/email_ticket.html', context)

    email = EmailMultiAlternatives(
        subject=f'Билет на мероприятие "{event.title}"',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_message, "text/html")
     
    if ticket.qr_code_image:
        qr_image = MIMEImage(ticket.qr_code_image)
        qr_image.add_header('Content-ID', '<qr_code>')
        email.attach(qr_image)

    return email.send(fail_silently=False)