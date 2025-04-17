from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from pyzbar.pyzbar import decode
from PIL import Image
from django.views import View
import cv2
import numpy as np

from tickets.forms import QRUploadForm
from events.models import Event
from tickets.models import Ticket
from tickets.utils import send_ticket_email


class RegisterForEventView(LoginRequiredMixin, View):
    template_name = 'tickets/ticket_email.html'
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        
        if Ticket.objects.filter(user=request.user, event=event).exists():
            return JsonResponse(
                {'status': 'error', 'message': 'Вы уже зарегистрированы на это мероприятие'},
                status=400
            )
        
        ticket = Ticket.objects.create(user=request.user, event=event)
        
        try:
            send_ticket_email(request, request.user, event, ticket)
            return render(self.request, self.template_name)
        except Exception as e:
            ticket.delete()
            return JsonResponse(
                {'status': 'error', 'message': 'Ошибка при отправке билета. Попробуйте позже.'},
                status=500
            )
        

class ScanTicketView(View):
    template_name = 'tickets/scanner.html'
    form_class = QRUploadForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            qr_image = request.FILES['qr_image']
            
            # Чтение изображения
            image_data = qr_image.read()
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Декодирование QR-кода
            decoded_objects = decode(img)
            
            if decoded_objects:
                qr_data = decoded_objects[0].data.decode('utf-8')
                
                try:
                    # Парсим данные из QR-кода (формат: EVENT:{event_id}:USER:{user_id}:CODE:{code})
                    parts = qr_data.split(':')
                    if len(parts) != 6:
                        raise ValueError
                        
                    _, event_id, _, user_id, _, code = parts
                    
                    ticket = Ticket.objects.get(
                        event_id=int(event_id),
                        user_id=int(user_id),
                        unique_code=code,
                        is_used=False
                    )
                    
                    # Отмечаем билет как использованный
                    ticket.mark_as_used()
                    
                    return render(request, self.template_name, {
                        'form': self.form_class(),
                        'success': True,
                        'ticket': ticket,
                        'user': ticket.user
                    })
                    
                except (ValueError, Ticket.DoesNotExist):
                    return render(request, self.template_name, {
                        'form': form,
                        'error': 'Недействительный или уже использованный билет'
                    })
            else:
                return render(request, self.template_name, {
                    'form': form,
                    'error': 'QR-код не найден на изображении'
                })
        
        return render(request, self.template_name, {'form': form})