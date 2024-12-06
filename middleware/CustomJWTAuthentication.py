# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.exceptions import AuthenticationFailed

# class CustomJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         # بررسی اینکه درخواست لاگین است یا نه
#         if request.path != '/authentication/login/' and request.method != 'POST':
#             cookie_token = request.COOKIES.get('access_token')
#             if cookie_token:
#                 # اضافه کردن توکن به هدر درخواست
#                 request.META['HTTP_AUTHORIZATION'] = f'Bearer {cookie_token}'
#         return super().authenticate(request)


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # اگر توکن در هدر موجود باشد یا متد احراز هویت نیاز به توکن داشته باشد
        if 'access_token' in request.COOKIES:
            # اضافه کردن توکن از کوکی به هدر
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {request.COOKIES["access_token"]}'

        # در غیر این صورت از کلاس والد استفاده کنید
        return super().authenticate(request)

