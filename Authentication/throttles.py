from rest_framework.throttling import SimpleRateThrottle

class SendVerificationCodeThrottle(SimpleRateThrottle):
    scope = 'send_verification_code'

    def get_cache_key(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return None
        return f'throttle_send_verification_code_{user.national_code}'