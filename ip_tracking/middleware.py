from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP


class IPTrackingMiddleware:
    """
    Middleware that:
    1. Blocks requests from blacklisted IPs.
    2. Logs allowed requests with IP, path, and timestamp.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP safely
        ip_address = request.META.get('REMOTE_ADDR')
        path = request.path
        timestamp = timezone.now()

        # 1️⃣ Block blacklisted IPs
        if ip_address and BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied: Your IP address is blocked.")

        # 2️⃣ Log the request
        if ip_address:
            RequestLog.objects.create(ip_address=ip_address, path=path, timestamp=timestamp)

        # Continue normal processing
        response = self.get_response(request)
        return response
