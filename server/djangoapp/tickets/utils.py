from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from io import BytesIO
import qrcode
from django.conf import settings

def send_ticket_email(request, user, event, ticket):
    """
    Отправка письма с билетом на мероприятие.
    """
    # Генерация QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(ticket.generate_qr_data())
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Создание HTML-письма
    context = {
        'user': user,
        'event': event,
        'ticket': ticket,
        'qr_code_data': ticket.generate_qr_data(),
    }
    html_message = render_to_string('tickets/ticket_email.html', context)

    email = EmailMultiAlternatives(
        subject=f'Билет на мероприятие "{event.title}"',
        body='',  # Текстовая версия
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_message, "text/html")
    
    # Прикрепляем QR-код как inline изображение
    email.attach('qr_code.png', buffer.read(), 'image/png')
    
    return email.send(fail_silently=False)