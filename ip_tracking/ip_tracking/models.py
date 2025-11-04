from django.db import models


class RequestLog(models.Model):
    """
    Stores details of every incoming request, including IP, path, timestamp, and geolocation.
    """
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"


class BlockedIP(models.Model):
    """
    Stores IP addresses that are blacklisted from accessing the system.
    """
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address
