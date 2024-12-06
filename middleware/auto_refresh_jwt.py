from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

# از مدل کاربر کاستوم‌شده استفاده می‌کنیم
User = get_user_model()

class AutoRefreshJWTMiddleware(MiddlewareMixin):
    """
    Middleware برای مدیریت توکن‌ها و احراز هویت
    """
    
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token') or request.headers.get('Authorization', '').split(' ')[-1]
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token or not refresh_token:
            # اگر هیچ‌کدام از توکن‌ها موجود نبودند، کاربر ناشناس در نظر گرفته می‌شود
            request.user = None
            return

        try:
            # تلاش برای اعتبارسنجی توکن دسترسی (access token)
            validated_token = AccessToken(access_token)
            national_code = validated_token.get('national_code')
            user = User.objects.get(national_code=national_code)
            request.user = user
            request.role = validated_token.get('role', 'unknown')

        except TokenError:
            # اگر توکن دسترسی منقضی شده باشد، در اینجا دسترسی به توکن رفرش برای تولید توکن جدید
            try:
                refresh = RefreshToken(refresh_token)
                new_access = refresh.access_token

                # بعد از این‌که توکن جدید ساخته شد، آن را در کوکی ذخیره می‌کنیم
                request._new_access_token = str(new_access)
                
                # ثبت اطلاعات کاربر و نقش
                national_code = new_access.get('national_code')
                user = User.objects.get(national_code=national_code)
                request.user = user
                request.role = new_access.get('role', 'unknown')

            except TokenError:
                # در صورت نامعتبر بودن refresh token، کاربر ناشناس
                request.user = None
                raise AuthenticationFailed("توکن معتبر نیست یا منقضی شده است.")
    
    def process_response(self, request, response):
        # بررسی می‌کنیم که آیا توکن جدیدی در درخواست هست
        new_access_token = getattr(request, '_new_access_token', None)
        if new_access_token:
            # اگر توکن جدید در درخواست موجود باشد، آن را در کوکی می‌گذاریم
            response.set_cookie(
                'access_token',
                new_access_token,
                httponly=True,
                secure=False if settings.DEBUG else True,
                samesite='Lax',
            )
            # همچنین می‌توانیم توکن جدید را در هدر Authorization بگذاریم
            response['Authorization'] = f'Bearer {new_access_token}'
        return response
