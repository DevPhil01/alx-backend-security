from django.utils import timezone
from .models import RequestLog

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip_address = request.META.get('REMOTE_ADDR')

        # Get path and timestamp
        path = request.path
        timestamp = timezone.now()

        # Save to database
        RequestLog.objects.create(ip_address=ip_address, path=path, timestamp=timestamp)

        response = self.get_response(request)
        return response
