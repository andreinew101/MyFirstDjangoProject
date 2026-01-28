from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from time import time
import threading

# Thread-safe dictionaries for tracking and banning
request_tracker = {}          # Track requests per IP per second
connection_tracker = {}       # Track concurrent connections per IP
banned_ips = {}               # Track temporarily banned IPs with unban time
tracker_lock = threading.Lock()

# Rate limit constants
MAX_CONCURRENT_CONNECTIONS = 3      # VERY aggressive - only 3 concurrent
MAX_REQUESTS_PER_SECOND = 2         # Only 2 requests per second
BAN_THRESHOLD = 5                   # Ban IP after 5 violations
BAN_DURATION = 60                   # Ban for 60 seconds
VIOLATION_WINDOW = 10               # Track violations over 10 seconds

class RateLimitMiddleware(MiddlewareMixin):
    """
    IP-based DoS protection with temporary IP banning.
    Designed to handle high-concurrency attacks.
    """
    
    def process_request(self, request):
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Only rate limit the /item_list endpoint
        if 'item' not in request.path.lower():
            return None
        
        current_time = time()
        
        with tracker_lock:
            # Check if IP is currently banned
            if ip in banned_ips and current_time < banned_ips[ip]:
                return HttpResponse(
                    f'IP temporarily banned for {int(banned_ips[ip] - current_time)}s (DoS detected)',
                    status=429
                )
            elif ip in banned_ips:
                # Ban expired, remove from banned list
                del banned_ips[ip]
            
            # Initialize trackers
            if ip not in request_tracker:
                request_tracker[ip] = {'requests': [], 'violations': 0, 'last_violation': 0}
            if ip not in connection_tracker:
                connection_tracker[ip] = 0
            
            # FIRST CHECK: Concurrent connections (most critical for DoS)
            if connection_tracker[ip] >= MAX_CONCURRENT_CONNECTIONS:
                self._record_violation(ip, current_time)
                return HttpResponse('429 Too Many Concurrent Connections', status=429)
            
            # SECOND CHECK: Requests per second
            request_tracker[ip]['requests'] = [
                req_time for req_time in request_tracker[ip]['requests']
                if current_time - req_time < 1.0
            ]
            
            if len(request_tracker[ip]['requests']) >= MAX_REQUESTS_PER_SECOND:
                self._record_violation(ip, current_time)
                return HttpResponse('429 Rate Limit Exceeded', status=429)
            
            # Check if too many violations in the window
            if request_tracker[ip]['violations'] >= BAN_THRESHOLD:
                banned_ips[ip] = current_time + BAN_DURATION
                return HttpResponse('429 IP Banned - DoS Attack Detected', status=429)
            
            # All checks passed - record request
            request_tracker[ip]['requests'].append(current_time)
            connection_tracker[ip] += 1
        
        request._client_ip = ip
        return None
    
    def _record_violation(self, ip, current_time):
        """Record a rate limit violation for this IP"""
        if ip not in request_tracker:
            request_tracker[ip] = {'requests': [], 'violations': 0, 'last_violation': 0}
        
        # Reset violations counter if outside window
        if current_time - request_tracker[ip]['last_violation'] > VIOLATION_WINDOW:
            request_tracker[ip]['violations'] = 0
        
        request_tracker[ip]['violations'] += 1
        request_tracker[ip]['last_violation'] = current_time
    
    def process_response(self, request, response):
        # Decrement concurrent connection count
        if hasattr(request, '_client_ip'):
            ip = request._client_ip
            with tracker_lock:
                if ip in connection_tracker:
                    connection_tracker[ip] = max(0, connection_tracker[ip] - 1)
        
        return response

