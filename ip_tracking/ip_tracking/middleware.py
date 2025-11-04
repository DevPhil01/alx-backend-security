from django.utils import timezone
from django.http import HttpResponseForbidden
from django.core.cache import cache
from ipgeolocation import IPGeolocationAPI
from .models import RequestLog, BlockedIP


class IPTrackingMiddleware:
    """
    Middleware that:
    1. Blocks requests from blacklisted IPs.
    2. Logs allowed requests with IP, path, timestamp, country, and city.
    3. Uses django-ipgeolocation with caching to avoid redundant lookups.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.geo = IPGeolocationAPI()

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        path = request.path
        timestamp = timezone.now()

        # 1️⃣ Block blacklisted IPs
        if ip_address and BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied: Your IP address is blocked.")

        # 2️⃣ Try to get geolocation data (with caching)
        country = city = None
        if ip_address:
            cache_key = f"geo_{ip_address}"
            geo_data = cache.get(cache_key)

            if not geo_data:
                try:
                    geo_info = self.geo.get_geolocation(ip_address)
                    country = geo_info.get('country_name')
                    city = geo_info.get('city')
                    cache.set(cache_key, {'country': country, 'city': city}, timeout=86400)  # 24 hours
                except Exception:
                    # API may fail or rate-limit; ignore and continue
                    pass
            else:
                country = geo_data.get('country')
                city = geo_data.get('city')

        # 3️⃣ Log the request
        if ip_address:
            RequestLog.objects.create(
                ip_address=ip_address,
                path=path,
                timestamp=timestamp,
                country=country,
                city=city
            )

        # Continue normal response
        response = self.get_response(request)
        return response
