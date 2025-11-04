# ip_tracking/models.py

from django.db import models
from django.utils import timezone


class RequestLog(models.Model):
    """
    Stores every incoming request with IP, timestamp, and path.
    Optionally includes country and city for geolocation.
    """
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"


class BlockedIP(models.Model):
    """
    Stores IP addresses that are manually or automatically blocked.
    """
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address


class SuspiciousIP(models.Model):
    """
    Stores IP addresses flagged as suspicious by anomaly detection.
    """
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField()
    detected_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"
