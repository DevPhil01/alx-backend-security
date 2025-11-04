# ip_tracking/tasks.py

from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from ip_tracking.models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    """
    Detects suspicious IPs based on abnormal activity.
    Runs hourly via Celery beat or cron.
    """
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    # Sensitive paths
    sensitive_paths = ['/admin', '/login']

    # Step 1: Find IPs exceeding 100 requests in the past hour
    heavy_users = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(request_count=models.Count('id'))
        .filter(request_count__gt=100)
    )

    for entry in heavy_users:
        ip = entry['ip_address']
        reason = f"Exceeded 100 requests in the past hour ({entry['request_count']} total)."
        SuspiciousIP.objects.get_or_create(ip_address=ip, defaults={'reason': reason})

    # Step 2: Find IPs accessing sensitive paths
    sensitive_hits = (
        RequestLog.objects.filter(path__in=sensitive_paths, timestamp__gte=one_hour_ago)
        .values_list('ip_address', flat=True)
        .distinct()
    )

    for ip in sensitive_hits:
        reason = "Accessed sensitive path (/admin or /login)."
        SuspiciousIP.objects.get_or_create(ip_address=ip, defaults={'reason': reason})
