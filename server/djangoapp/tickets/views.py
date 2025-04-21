import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.views import View
from pyzbar.pyzbar import decode
from django.contrib.auth.mixins import LoginRequiredMixin


from tickets.forms import QRUploadForm
from tickets.models import Ticket


class ScanTicketView(LoginRequiredMixin, View):
    login_url = '/users/login/'
    template_name = 'tickets/scan.html'
    form_class = QRUploadForm

    def get(self, request):
        user = request.user
        if not user.is_staff:
            return redirect('/')
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
                        'user': ticket.user,
                        'coins_added': ticket.event.coins_reward if ticket.event.coins_reward > 0 else None
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