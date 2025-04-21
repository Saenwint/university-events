from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('admin:login')}?next={request.path}")
            
            admin_emails = getattr(settings, 'ADMIN_LIST', [])
            if request.user.email not in admin_emails:
                messages.error(request, "Доступ запрещён")
                return redirect('home')
        
        return self.get_response(request)