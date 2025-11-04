from django.shortcuts import render
# ip_tracking/views.py

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit

@csrf_exempt
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def anonymous_login_view(request):
    """
    Login view for anonymous users, rate-limited to 5 requests per minute per IP.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'POST method required'}, status=400)


@csrf_exempt
@ratelimit(key='user', rate='10/m', method='POST', block=True)
def authenticated_sensitive_view(request):
    """
    A sensitive endpoint for authenticated users only.
    Limited to 10 requests per minute per user.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=403)
    
    # Example: return some protected data
    return JsonResponse({'message': 'You have access to this sensitive data'})
